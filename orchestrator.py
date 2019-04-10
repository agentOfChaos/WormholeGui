from transitions import Machine


class TransferMode:
    Text, File = range(2)


class WormholeOrchestrator:

    states = ["error", "disconnected", "welcome_wait", "idle", "code_wait", "code_ready", "receiver_wait", "sender_wait",
              "receiver_wait_verify", "receiver_connected", "sending_message", "msg_ack_wait", "file_ack_wait",
              "uploading", "upload_failed", "wormhole_error", "sender_wait_verify", "sender_connected", "offered", "downloading", "download_failed"]

    def __init__(self, app, stargate, stats):
        self.app = app
        self.stargate = stargate
        self.stats = stats

        self.tmp_text = ""
        self.tmp_filename = ""
        self.transfer_mode = TransferMode.Text

        self.machine = Machine(model=self, states=self.states, initial="disconnected")

        self.machine.add_transition("error", self.states, "error", before="_on_error")
        self.machine.add_transition("msg_error", ["msg_ack_wait", "file_ack_wait"], "wormhole_error", before="_on_wormhole_error")

        self.machine.add_transition("connect", "disconnected", "welcome_wait", before="_perform_connection")

        self.machine.add_transition("got_welcome", "welcome_wait", "idle", before="_finish_connection")
        self.machine.add_transition("set_code", "idle", "code_wait", after="_set_code")
        self.machine.add_transition("set_code", "code_ready", "code_ready", after="_set_code_again")
        self.machine.add_transition("got_code", "code_wait", "code_ready", after="_got_code")

        self.machine.add_transition("send_message", "code_ready", "receiver_wait", after="_send_msg")
        self.machine.add_transition("got_transit", "receiver_wait", "receiver_wait", before="_process_transit_send")
        self.machine.add_transition("got_transit", "receiver_wait_verify", "receiver_wait_verify", before="_process_transit_send")
        self.machine.add_transition("got_transit", "receiver_connected", "receiver_connected", before="_process_transit_send")
        self.machine.add_transition("got_transit", "file_ack_wait", "file_ack_wait", before="_process_transit_send")
        self.machine.add_transition("got_unverified_key", "receiver_wait", "receiver_wait_verify")
        self.machine.add_transition("got_verifier", "receiver_wait_verify", "receiver_connected", before="_got_verifier", after="_continue_up_transfer")
        self.machine.add_transition("continue_sending_message", "receiver_connected", "msg_ack_wait", before="_continue_msg_transfer")
        self.machine.add_transition("got_answer", "msg_ack_wait", "idle", after="_process_msg_answer")

        self.machine.add_transition("send_file", "code_ready", "receiver_wait", after="_send_file")
        self.machine.add_transition("continue_sending_file", "receiver_connected", "file_ack_wait", before="_continue_file_transfer")
        self.machine.add_transition("got_answer", "file_ack_wait", "uploading", after="_process_file_answer")
        self.machine.add_transition("fail_upload", "uploading", "upload_failed", after="_upload_failure")
        self.machine.add_transition("complete_upload", "uploading", "idle", after="_upload_success")

        self.machine.add_transition("receive", "code_ready", "sender_wait", after="_recv_any")
        self.machine.add_transition("got_transit", "sender_wait", "sender_wait", before="_process_transit_recv")
        self.machine.add_transition("got_transit", "sender_wait_verify", "sender_wait_verify", before="_process_transit_recv")
        self.machine.add_transition("got_transit", "sender_connected", "sender_connected", before="_process_transit_recv")
        self.machine.add_transition("got_unverified_key", "sender_wait", "sender_wait_verify")
        self.machine.add_transition("got_verifier", "sender_wait_verify", "sender_connected", before="_got_verifier")
        self.machine.add_transition("got_message_offer", "sender_connected", "idle", after="_process_message_offer")
        self.machine.add_transition("got_file_offer", "sender_connected", "downloading", after="_process_file_offer")
        self.machine.add_transition("fail_download", "downloading", "download_failed", after="_download_failure")
        self.machine.add_transition("complete_download", "downloading", "idle", after="_download_success")

    def _on_error(self, desc=None):
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = True
        msg = "Logic error in state %s" % self.state
        if desc is not None:
            msg += "\nDescription: " + str(desc)
        self.app.custom_error(msg)

    def _on_wormhole_error(self, message):
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = True
        self.app.custom_error("Wormhole error in state %s:\n%s" % (self.state, str(message)))

    def _perform_connection(self):
        self.stargate.connect()
        self.stats.wormhole_connected = False

    def _finish_connection(self, welcome):
        self.stats.wormhole_connected = True
        self.app.update_wormhole_action_text()

    def _set_code(self, code):
        self.stargate.set_code(code)
        self.stats.code_locked = False

    def _set_code_again(self, code):
        self.stargate.disconnect()
        self.stargate.connect()
        self._set_code(code)

    def _got_code(self, code):
        self.app.got_secret_code(code)
        self.stats.code_locked = True

    def _process_transit_recv(self, transit):
        self.stargate.handle_transit_recv(transit)

    def _process_transit_send(self, transit):
        self.stargate.handle_transit_send(transit)

    def _send_msg(self, text):
        self.tmp_text = text
        self.transfer_mode = TransferMode.Text
        self.stats.waiting_peer = True
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = False

    def _send_file(self, filename):
        self.tmp_filename = filename
        self.transfer_mode = TransferMode.File
        self.stats.waiting_peer = True
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = False

    def _got_verifier(self, verifier):
        self.stats.waiting_peer = False
        self.stats.peer_connected = True

    def _continue_up_transfer(self, verifier):
        if self.transfer_mode == TransferMode.Text:
            self.continue_sending_message()
        elif self.transfer_mode == TransferMode.File:
            self.continue_sending_file()
        else:
            self.error()

    def _continue_msg_transfer(self):
        self.stargate.send_message(self.tmp_text)
        self.stats.msgs_sent += 1
        self.stats.upload_running = True

    def _continue_file_transfer(self):
        self.stargate.send_file(self.tmp_filename)
        self.stats.files_sent += 1
        self.stats.upload_running = True

    def _process_msg_answer(self, answer):
        if "message_ack" in answer:
            if answer["message_ack"] == "ok":
                self.stats.msgs_acks += 1
                self.stats.peer_connected = False
                self.stats.upload_running = False
                self.stats.last_transfer_ok = True
                self.stats.last_transfer_fail = False
                return
        self.error()

    def _process_file_answer(self, answer):
        if "file_ack" in answer:
            if answer["file_ack"] == "ok":
                self.stargate.finish_sending_file(self.tmp_filename, self.app.send_progress_callback)
                return
        self.error()

    def _upload_failure(self):
        self.stats.upload_running = False
        self.stats.peer_connected = False
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = True
        self.stats.send_errors += 1

    def _upload_success(self):
        self.stats.last_transfer_ok = True
        self.stats.last_transfer_fail = False
        self.stats.upload_running = False
        self.stats.peer_connected = False

    def _recv_any(self):
        self.stats.waiting_peer = True
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = False

    def _process_message_offer(self, offer):
        self.app.recv_message_callback(offer["message"])
        self.stargate.ack_message()
        self.stats.last_transfer_ok = True
        self.stats.last_transfer_fail = False
        self.stats.upload_running = False
        self.stats.peer_connected = False

    def _process_file_offer(self, offer):
        filename = offer["file"]["filename"]
        filesize = offer["file"]["filesize"]
        self.app.recv_offered_callback(filename, filesize)
        self.stats.peer_connected = True
        self.stats.download_running = True
        self.stargate.download_file(filename, filesize, self.app.recv_progress_callback)

    def _download_failure(self):
        self.stats.download_running = False
        self.stats.peer_connected = False
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = True
        self.stats.recv_errors += 1

    def _download_success(self):
        self.stats.last_transfer_ok = True
        self.stats.last_transfer_fail = False
        self.stats.download_running = False
        self.stats.peer_connected = False
