from twisted.internet import reactor
import wormhole
import json
import os
import hashlib
from binascii import hexlify
from time import sleep

from twisted.internet.defer import inlineCallbacks
from wormhole.transit import TransitSender, TransitReceiver
from twisted.protocols import basic



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

    def __init__(self, config, stats, logger, code_callback=None, progress_callback=None, message_callback=None, offered_callback=None):
        self.config = config
        self.stats = stats
        self.logger = logger
        self.wormhole = None
        self.code_callback = code_callback
        self.progress_callback = progress_callback
        self.message_callback = message_callback
        self.offered_callback = offered_callback
        self.code = ""
        self.reactor = reactor
        self.transit_sender = None
        self.transit_receiver = None
        self.file_to_send = ""
        self.file_to_receive = ""
        self.filesize_to_receive = 0
        self.wants_answer = False
        self.wants_offet = False
        self.got_unverified_key = False
        self.got_verifier = False
        self.got_peer_callback = None
        self.connected = False
        self.receive_mode = False

    @property
    def connected(self):
        return self.stats.wormhole_connected

    @connected.setter
    def connected(self, value):
        self.stats.wormhole_connected = value


    def connect(self):
        self.logger.info("Connecting to relay: %s" % self.config["wormhole"]["relay"])
        self.wormhole = wormhole.create(self.config["wormhole"]["appid"],
                                        self.config["wormhole"]["relay"],
                                        self.reactor,
                                        delegate=self)
        self.connected = True

    def disconnect(self):
        self.wormhole.close()
        self.connected = False
        self.logger.info("Disconnected from relay")

    def reconnect_as_needed(self):
        if self.connected:
            if self.code != "":
                self.disconnect()
                self.connect()
        else:
            self.connect()

    def allocate_code(self):
        self.reconnect_as_needed()
        self.wormhole.allocate_code(3)

    def set_code(self, code):
        self.reconnect_as_needed()
        self.wormhole.set_code(code)

    def send_message(self, data: str):
        def closure():
            self.inner_send_message(data)
        self.logger.info("Waiting for peer...")
        self.stats.waiting_peer = True
        self.got_peer_callback = closure
        self.check_peer_available()

    def inner_send_message(self, data: str):
        self.send_data({"offer": {"message": data}})
        self.wants_answer = True
        self.stats.msgs_sent += 1

    def send_file(self, filepath: str):
        def closure():
            self.inner_send_file(filepath)
        self.logger.info("Waiting for peer...")
        self.stats.waiting_peer = True
        self.got_peer_callback = closure
        self.check_peer_available()

    @inlineCallbacks
    def inner_send_file(self, filepath: str):
        self.stats.upload_running = True
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
        self.wants_answer = True
        self.file_to_send = filepath

        self.logger.info("Transmission sequence has begun, file: %s" % self.file_to_send)
        self.stats.files_sent += 1

    @inlineCallbacks
    def finish_sending_file(self):
        self.logger.info("Trasmission sequence entering phase 2")
        with open(self.file_to_send, "rb") as fp:
            fp.seek(0, 2)
            filesize = fp.tell()
            fp.seek(0, 0)

            self.logger.debug("Connecting to transit relay %s ..." % self.config["wormhole"]["transit"])
            record_pipe = yield self.transit_sender.connect()
            self.logger.debug("Transit connected")
            self.logger.info("Sending (%s).." % record_pipe.describe())

            hasher = hashlib.sha256()

            total_transferred = 0
            count_and_hash = lambda data: _count_and_hash(data, total_transferred)

            def _count_and_hash(data, total_transferred):
                hasher.update(data)
                total_transferred = total_transferred + len(data)
                if self.progress_callback is not None: self.progress_callback((total_transferred*100)/filesize, self.file_to_send)
                return data

            self.logger.info("Transmitting file...")
            fs = basic.FileSender()
            yield fs.beginFileTransfer(fp, record_pipe, transform=count_and_hash)

            expected_hash = hasher.digest()
            expected_hex = bytes_to_hexstr(expected_hash)
            self.logger.info("File sent, awaiting for confirmation...")

            ack_bytes = yield record_pipe.receive_record()
            record_pipe.close()
            ack = json.loads(ack_bytes.decode("utf-8"))
            ok = ack.get("ack", u"")
            if ok != "ok":
                self.stats.send_errors += 1
                self.logger.error("Confirmation not understood. Transfer unsuccessful.")
                self.reset_transfer()
                return
            if "sha256" in ack:
                if ack["sha256"] != expected_hex:
                    self.stats.send_errors += 1
                    self.logger.error("Wrong checksum. The file was damaged during transport.")
                    self.reset_transfer()
                    return
            self.logger.info("Confirmation received. Transfer complete.")
            self.stats.upload_running = False
            self.stats.peer_connected = False
            self.reset_transfer()

    def reset_transfer(self):
        self.file_to_send = ""
        self.file_to_receive = ""
        self.filesize_to_receive = 0
        self.wants_answer = False
        self.got_unverified_key = False
        self.got_verifier = False
        self.wants_offer = False
        self.receive_mode = False

    def send_data(self, data: dict):
        message = json.dumps(data)
        self.logger.debug("Wormhole send: " + message)
        self.wormhole.send_message(message.encode("utf-8"))

    def wormhole_got_code(self, code):
        self.code = code
        self.stats.code_locked = True
        if self.code_callback is not None: self.code_callback(code)

    def wormhole_got_message(self, msg):  # called for each message
        self.logger.info("Wormhole got message: " + str(msg.decode("utf-8")))
        self.parse_message(msg)

    def wormhole_got_welcome(self, welcome):
        self.logger.info("Wormhole got welcome: " + str(welcome))

    def wormhole_got_unverified_key(self, key):
        self.got_unverified_key = True
        self.logger.info("Wormhole got unverified key: " + str(key))

    def wormhole_got_versions(self, versions):
        self.logger.info("Wormhole got version: " + str(versions))

    def wormhole_got_verifier(self, verifier):
        self.got_verifier = True
        self.logger.info("Wormhole got verifier: " + str(verifier))
        if self.receive_mode:
            pass  # todo optional verify
        self.check_peer_available()

    def wormhole_closed(self, result):
        pass

    def check_peer_available(self):
        if self.got_verifier and self.got_unverified_key:
            if self.got_peer_callback is not None:
                self.logger.info("Peer connected!")
                self.stats.peer_connected = True
                self.got_peer_callback()
                self.got_peer_callback = None
                self.got_unverified_key = False
                self.got_verifier = False

    def parse_message(self, msg):
        try:
            msg_obj = json.loads(msg.decode("utf-8"))
            if "answer" in msg_obj and not self.receive_mode:
                self.handle_answer(msg_obj["answer"])
            if "offer" in msg_obj and self.receive_mode:
                self.handle_offer(msg_obj["offer"])
            if "transit" in msg_obj:
                if self.receive_mode:
                    self.handle_transit_recv(msg_obj["transit"])
                else:
                    self.transit_sender.add_connection_hints(msg_obj["transit"].get("hints-v1", []))
            if "error" in msg_obj:
                self.stats.recv_errors += 1
                self.reset_transfer()

        except Exception:
            self.stats.recv_errors += 1
            self.reset_transfer()


    def handle_answer(self, answer):
        if not self.wants_answer:
            return  # duplicate answer

        if "message_ack" in answer:
            if answer["message_ack"] == "ok":
                self.stats.msgs_acks += 1
                self.stats.peer_connected = False
        if "file_ack" in answer:
            if answer["file_ack"] == "ok":
                self.stats.file_acks += 1

        if self.file_to_send != "":
            self.finish_sending_file()

        self.wants_answer = False

    @inlineCallbacks
    def handle_offer(self, offer):
        if not self.wants_offer:
            return  # duplicate offer

        if "message" in offer:
            if self.message_callback is not None:
                self.message_callback(offer["message"])
            self.send_data({"answer": {"message_ack": "ok"}})
            self.stats.peer_connected = False
        if "file" in offer:
            self.stats.download_running = True
            self.file_to_receive = os.path.join(self.config["app"]["download_folder"], offer["file"]["filename"])
            self.filesize_to_receive = int(offer["file"]["filesize"])

            self.logger.info("Offered file: %s, %d bytes." % (self.file_to_receive, self.filesize_to_receive))

            if self.offered_callback is not None:
                if not self.offered_callback(self.file_to_receive, self.filesize_to_receive):
                    return

            free = estimate_free_space(self.file_to_receive)

            if free is not None and free < self.filesize_to_receive:
                self.logger.error("Error: insufficient free space (%sB) for file (%sB)" % (free, self.filesize_to_receive))
                self.reset_transfer()
                return

            self.send_data({"answer": {"file_ack": "ok"}})

            self.logger.debug("Connecting to transit relay %s ..." % self.config["wormhole"]["transit"])
            record_pipe = yield self.transit_receiver.connect()
            self.logger.info("Receiving (%s).." % record_pipe.describe())

            total_transferred = 0
            count_and_hash = lambda partial_transferred: _count_and_hash(partial_transferred, total_transferred)

            def _count_and_hash(partial_transferred, total_transferred):
                total_transferred = total_transferred + partial_transferred
                if self.progress_callback is not None: self.progress_callback((total_transferred * 100) / self.filesize_to_receive,
                                                                              self.file_to_receive)
                return partial_transferred

            self.logger.info("Receiving data...")
            hasher = hashlib.sha256()
            with open(self.file_to_receive, "wb") as fp:
                received = yield record_pipe.writeToFile(fp, self.filesize_to_receive, count_and_hash, hasher.update)
                datahash = hasher.digest()
                datahash_hex = bytes_to_hexstr(datahash)
                ack = {"ack": "ok", "sha256": datahash_hex}
                yield record_pipe.send_record(json.dumps(ack).encode("utf-8"))
                yield record_pipe.close()

                self.logger.info("Done receiving data!")
            self.stats.download_running = False
            self.stats.peer_connected = False

        self.wants_offer = False

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

    def receive_any(self):
        self.wants_offer = True
        self.receive_mode = True


