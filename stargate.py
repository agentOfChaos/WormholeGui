from twisted.internet import reactor
import wormhole
import json
import os
import hashlib
from binascii import hexlify
from typing import Callable, Any

from twisted.internet.error import ConnectionClosed
from twisted.internet.defer import inlineCallbacks
from wormhole.transit import TransitSender, TransitReceiver
from wormhole.errors import KeyFormatError
from twisted.protocols import basic

from utils import has_orchestrator_error_message


def bytes_to_hexstr(b):
    assert isinstance(b, type(b""))
    hexstr = hexlify(b).decode("ascii")
    assert isinstance(hexstr, type(u""))
    return hexstr


def estimate_free_space(target):
    # f_bfree is the blocks available to a root user. It might be more
    # accurate to use f_bavail (blocks available to non-root user), but we
    # don't know which user is running us, and a lot of installations don't
    # bother with reserving extra space for root, so let's just stick to the
    # basic (larger) estimate.
    try:
        s = os.statvfs(os.path.dirname(os.path.abspath(target)))
        return s.f_frsize * s.f_bfree
    except AttributeError:
        return None



class StarGate:

    def __init__(self, config, logger):
        self.config = config
        self.orchestrator = None
        self.logger = logger
        self.wormhole = None
        self.code = ""
        self.reactor = reactor
        self.transit_sender = None
        self.transit_receiver = None
        self.file_sender = None
        self.fp = None

    def connect(self):
        self.logger.info("Connecting to relay: %s" % self.config["wormhole"]["relay"])
        self.wormhole = wormhole.create(self.config["wormhole"]["appid"],
                                        self.config["wormhole"]["relay"],
                                        self.reactor,
                                        delegate=self)

    def disconnect(self):
        self.wormhole.close()

    def set_code(self, code):
        try:
            self.wormhole.set_code(code)
        except KeyFormatError as e:
            self.orchestrator.got_bad_code(str(e))


    def send_message(self, data: str):
        self.send_data({"offer": {"message": data}})

    @inlineCallbacks
    def send_file(self, filepath: str):
        self.transit_sender = TransitSender(self.config["wormhole"]["transit"], no_listen=True, reactor=self.reactor)
        sender_abilities = self.transit_sender.get_connection_abilities()
        sender_hints = yield self.transit_sender.get_connection_hints()
        sender_transit = {
            "abilities-v1": sender_abilities,
            "hints-v1": sender_hints,
        }
        self.send_data({"transit": sender_transit})

        self.logger.debug("Setting transit key...")
        transit_key = self.wormhole.derive_key(self.config["wormhole"]["appid"] + "/transit-key",
                                               self.transit_sender.TRANSIT_KEY_LENGTH)
        self.transit_sender.set_transit_key(transit_key)

        filename = os.path.basename(os.path.normpath(filepath))
        filesize = os.stat(filepath).st_size
        message_offer = {"offer": {"file": {"filename": filename, "filesize": filesize}}}
        self.send_data(message_offer)
        self.file_to_send = filepath

        self.logger.info("Transmission sequence has begun, file: %s" % self.file_to_send)

    @inlineCallbacks
    def finish_sending_file(self, filepath: str, progress_callback: Callable[[int, int, str, str], Any]):
        self.logger.info("Trasmission sequence entering phase 2")
        with open(filepath, "rb") as fp:
            fp.seek(0, 2)
            filesize = fp.tell()
            fp.seek(0, 0)

            self.logger.debug("Connecting to transit relay %s ..." % self.config["wormhole"]["transit"])
            record_pipe = yield self.transit_sender.connect()
            self.logger.debug("Transit connected")
            self.logger.info("Sending (%s).." % record_pipe.describe())

            hasher = hashlib.sha256()

            total_transferred = [0]
            count_and_hash = lambda data: _count_and_hash(data, total_transferred)

            def _count_and_hash(data, total_transferred):
                hasher.update(data)
                total_transferred[0] = total_transferred[0] + len(data)
                if progress_callback is not None:
                    progress_callback(total_transferred[0], filesize, self.file_to_send, record_pipe.describe())
                return data

            self.logger.info("Transmitting file...")
            self.file_sender = basic.FileSender()
            try:
                yield self.file_sender.beginFileTransfer(fp, record_pipe, transform=count_and_hash)
            except Exception:
                self.logger.warning.info("Transfer interrupted.")
                self.orchestrator.fail_upload()
                return

            expected_hash = hasher.digest()
            expected_hex = bytes_to_hexstr(expected_hash)
            self.logger.info("File sent, awaiting for confirmation...")

            ack_bytes = yield record_pipe.receive_record()
            record_pipe.close()
            ack = json.loads(ack_bytes.decode("utf-8"))
            ok = ack.get("ack", u"")
            if ok != "ok":
                self.logger.error("Confirmation not understood. Transfer unsuccessful.")
                self.orchestrator.fail_upload()
                return
            if "sha256" in ack:
                if ack["sha256"] != expected_hex:
                    self.logger.error("Wrong checksum. The file was damaged during transport.")
                    self.orchestrator.fail_upload()
                    return
            self.logger.info("Confirmation received. Transfer complete.")
            self.orchestrator.complete_upload()

    def ack_message(self):
        self.send_data({"answer": {"message_ack": "ok"}})

    def ack_file(self):
        self.send_data({"answer": {"file_ack": "ok"}})

    def send_data(self, data: dict):
        message = json.dumps(data)
        self.logger.debug("Wormhole send: " + message)
        self.wormhole.send_message(message.encode("utf-8"))

    @has_orchestrator_error_message
    def wormhole_got_code(self, code):
        self.orchestrator.got_code(code)
        self.code = code

    def wormhole_got_message(self, msg):  # called for each message
        self.logger.info("Wormhole got message: " + str(msg.decode("utf-8")))
        self.parse_message(msg)

    @has_orchestrator_error_message
    def wormhole_got_welcome(self, welcome):
        self.logger.info("Wormhole got welcome: " + str(welcome))
        self.orchestrator.got_welcome(welcome)

    @has_orchestrator_error_message
    def wormhole_got_unverified_key(self, key):
        self.orchestrator.got_unverified_key(key)

    def wormhole_got_versions(self, versions):
        self.logger.info("Wormhole got version: " + str(versions))

    @has_orchestrator_error_message
    def wormhole_got_verifier(self, verifier):
        self.logger.info("Wormhole got verifier: " + str(verifier))
        self.orchestrator.got_verifier(verifier)

    @has_orchestrator_error_message
    def wormhole_closed(self, result):
        self.logger.info("Wormhole got closed: " + str(result))
        self.orchestrator.got_disconnected()

    @has_orchestrator_error_message
    def parse_message(self, msg):
        try:
            msg_obj = json.loads(msg.decode("utf-8"))
            if "answer" in msg_obj:
                self.orchestrator.got_answer(msg_obj["answer"])
            if "offer" in msg_obj:
                self.handle_offer(msg_obj["offer"])
            if "transit" in msg_obj:
                self.orchestrator.got_transit(msg_obj["transit"])
            if "error" in msg_obj:
                self.orchestrator.error(msg_obj["error"])

        except Exception as e:
            self.orchestrator.error(str(e))

    @has_orchestrator_error_message
    def handle_offer(self, offer):
        if "message" in offer:
            self.orchestrator.got_message_offer(offer)
        if "file" in offer:
            self.orchestrator.got_file_offer(offer)

    @inlineCallbacks
    def download_file(self, filename, filesize, progress_callback: Callable[[int, int, str, str], Any] = None):
        self.logger.info("Offered file: %s, %d bytes." % (filename, filesize))

        free = estimate_free_space(filename)

        if free is not None and free < filesize:
            self.logger.error("Error: insufficient free space (%sB) for file (%sB)" % (free, filesize))
            self.orchestrator.fail_download()
            return

        self.ack_file()

        self.logger.debug("Connecting to transit relay %s ..." % self.config["wormhole"]["transit"])
        record_pipe = yield self.transit_receiver.connect()
        self.logger.info("Receiving (%s).." % record_pipe.describe())

        total_transferred = [0]
        count_and_hash = lambda partial_transferred: _count_and_hash(partial_transferred, total_transferred)

        def _count_and_hash(partial_transferred, total_transferred):
            total_transferred[0] = total_transferred[0] + partial_transferred
            if progress_callback is not None:
                progress_callback(total_transferred[0], filesize, filename, record_pipe.describe())
            return partial_transferred

        self.logger.info("Receiving data...")
        hasher = hashlib.sha256()
        with open(os.path.join(self.config["app"]["download_folder"], filename), "wb") as self.fp:
            try:
                received = yield record_pipe.writeToFile(self.fp, filesize, count_and_hash, hasher.update)
                datahash = hasher.digest()
                datahash_hex = bytes_to_hexstr(datahash)
                ack = {"ack": "ok", "sha256": datahash_hex}
                yield record_pipe.send_record(json.dumps(ack).encode("utf-8"))
            except ConnectionClosed:
                self.logger.warning("Connection lost, transfer interrupted.")
                self.orchestrator.fail_download()
            yield record_pipe.close()

            self.logger.info("Done receiving data!")
            self.orchestrator.complete_download()
        self.fp = None


    @inlineCallbacks
    def handle_transit_recv(self, sender_transit):
        self.transit_receiver = TransitReceiver(self.config["wormhole"]["transit"], no_listen=True, reactor=self.reactor)
        transit_key = self.wormhole.derive_key(self.config["wormhole"]["appid"] + "/transit-key",
                                               self.transit_receiver.TRANSIT_KEY_LENGTH)
        self.transit_receiver.set_transit_key(transit_key)

        self.transit_receiver.add_connection_hints(sender_transit.get("hints-v1", []))
        receiver_abilities = self.transit_receiver.get_connection_abilities()
        receiver_hints = yield self.transit_receiver.get_connection_hints()
        receiver_transit = {
            "abilities-v1": receiver_abilities,
            "hints-v1": receiver_hints,
        }

        self.send_data({"transit": receiver_transit})

    def handle_transit_send(self, transit):
        self.transit_sender.add_connection_hints(transit.get("hints-v1", []))

    def stop_all(self):
        if self.fp is not None:
            self.fp.close()
        try:
            self.file_sender.stopProducing()
        except AttributeError:
            pass
        try:
            self.transit_receiver.close()
        except AttributeError:
            pass
        try:
            self.transit_sender.close()
        except AttributeError:
            pass
        try:
            self.wormhole.close()
        except AttributeError:
            pass
