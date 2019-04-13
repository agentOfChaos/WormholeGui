try:
    import pygraphviz
    from transitions.extensions import GraphMachine as Machine
    has_graph_capab = True
except Exception:
    from transitions import Machine
    has_graph_capab = False


from utils import open_file
from PySide2.QtWidgets import QMessageBox


class TransferMode:
    Text, File = range(2)


class WormholeOrchestrator:

    states = ["error", "disconnected", "welcome_wait", "hot_welcome_wait",  "hot_welcome_wait_recv", "idle",
              "code_wait", "code_wait_recv", "code_ready", "wait_for_receiver", "wait_for_sender",
              "wait_for_receiver_verify", "receiver_connected", "msg_ack_wait", "file_ack_wait",
              "uploading", "wormhole_error", "wait_for_sender_verify", "sender_connected", "downloading",
              "wait_for_early_receiver_verify", "transitory_disconnecting"]

    debug_graph_path = "debug.png"

    def __init__(self, app, stargate, stats):
        self.app = app
        self.stargate = stargate
        self.stats = stats

        self.tmp_text = ""
        self.tmp_filename = ""
        self.tmp_code = ""
        self.tmp_error = {}

        self.transfer_mode = TransferMode.Text

        self.machine = Machine(model=self, states=self.states, initial="disconnected")

        self.machine.add_transition("error", self.states, "error", before="_on_error_before", after="_on_error_after")
        self.machine.add_transition("rearm", "error", "disconnected", before="_on_rearm")
        self.machine.add_transition("connect", "error", "error")
        self.machine.add_transition("disconnect", "error", "error")
        self.machine.add_transition("got_welcome", "error", "error")
        self.machine.add_transition("got_disconnected", "error", "error")
        self.machine.add_transition("receive", "error", "error")
        self.machine.add_transition("set_code", "error", "error")
        self.machine.add_transition("got_code", "error", "error")
        self.machine.add_transition("got_bad_code", "error", "error")
        self.machine.add_transition("send_message", "error", "error")
        self.machine.add_transition("got_transit", "error", "error")
        self.machine.add_transition("got_unverified_key", "error", "error")
        self.machine.add_transition("got_verifier", "error", "error")
        self.machine.add_transition("continue_sending_message", "error", "error")
        self.machine.add_transition("got_answer", "error", "error")
        self.machine.add_transition("send_file", "error", "error")
        self.machine.add_transition("continue_sending_file", "error", "error")
        self.machine.add_transition("fail_upload", "error", "error")
        self.machine.add_transition("send_file", "error", "error")
        self.machine.add_transition("complete_upload", "error", "error")
        self.machine.add_transition("got_message_offer", "error", "error")
        self.machine.add_transition("got_file_offer", "error", "error")
        self.machine.add_transition("fail_download", "error", "error")
        self.machine.add_transition("complete_download", "error", "error")

        self.machine.add_transition("msg_error", ["msg_ack_wait", "file_ack_wait"], "wormhole_error", before="_on_wormhole_error")

        self.machine.add_transition("connect", "disconnected", "welcome_wait", before="_perform_connection")

        self.machine.add_transition("got_welcome", "welcome_wait", "idle", before="_finish_connection")
        self.machine.add_transition("got_welcome", "hot_welcome_wait", "code_wait", after="_finish_hot_connection")
        self.machine.add_transition("got_welcome", "hot_welcome_wait_recv", "code_wait_recv", after="_finish_hot_connection")
        self.machine.add_transition("got_disconnected", list(filter(lambda s: s != "transitory_disconnecting", self.states)),
                                    "disconnected", after="_finish_disconnection")
        self.machine.add_transition("got_disconnected", "transitory_disconnecting", "hot_welcome_wait", after="_perform_connection")

        self.machine.add_transition("set_code", "idle", "code_wait", after="_set_code")
        self.machine.add_transition("set_code", "code_ready", "transitory_disconnecting", before="_save_tmp_code", after="_set_code_again")
        self.machine.add_transition("set_code", "disconnected", "hot_welcome_wait", before="_save_tmp_code", after="_perform_connection")

        self.machine.add_transition("receive", "idle", "code_wait_recv", after="_set_code")
        self.machine.add_transition("receive", "wait_for_sender", "wait_for_sender", after="_set_code_again")
        self.machine.add_transition("receive", "disconnected", "hot_welcome_wait_recv", before="_save_tmp_code", after="_perform_connection")

        self.machine.add_transition("got_code", "code_wait", "code_ready", after="_got_code")
        self.machine.add_transition("got_bad_code", "code_wait", "idle", after="_got_bad_code")
        self.machine.add_transition("got_code", "code_wait_recv", "wait_for_sender", before="_got_code", after="_recv_any")

        self.machine.add_transition("send_message", "code_ready", "wait_for_receiver", after="_send_msg")
        self.machine.add_transition("send_message", "receiver_connected", "receiver_connected", before="_send_msg", after="_continue_msg_transfer")

        self.machine.add_transition("got_transit", "wait_for_receiver", "wait_for_receiver", before="_process_transit_send")
        self.machine.add_transition("got_transit", "wait_for_receiver_verify", "wait_for_receiver_verify", before="_process_transit_send")
        self.machine.add_transition("got_transit", "receiver_connected", "receiver_connected", before="_process_transit_send")
        self.machine.add_transition("got_transit", "file_ack_wait", "file_ack_wait", before="_process_transit_send")

        self.machine.add_transition("got_unverified_key", "wait_for_receiver", "wait_for_receiver_verify")
        self.machine.add_transition("got_unverified_key", "code_ready", "wait_for_early_receiver_verify")
        self.machine.add_transition("got_verifier", "wait_for_receiver_verify", "receiver_connected", before="_got_verifier", after="_continue_up_transfer")
        self.machine.add_transition("got_verifier", "wait_for_early_receiver_verify", "receiver_connected", before="_got_verifier")

        self.machine.add_transition("continue_sending_message", "receiver_connected", "msg_ack_wait", before="_continue_msg_transfer")
        self.machine.add_transition("got_answer", "msg_ack_wait", "idle", after="_process_msg_answer")

        self.machine.add_transition("send_file", "code_ready", "wait_for_receiver", after="_send_file")
        self.machine.add_transition("send_file", "receiver_connected", "receiver_connected", before="_send_file", after="_continue_up_transfer")
        self.machine.add_transition("continue_sending_file", "receiver_connected", "file_ack_wait", before="_continue_file_transfer")
        self.machine.add_transition("got_answer", "file_ack_wait", "uploading", after="_process_file_answer")
        self.machine.add_transition("fail_upload", "uploading", "idle", after="_upload_failure")
        self.machine.add_transition("complete_upload", "uploading", "idle", after="_upload_success")

        self.machine.add_transition("got_transit", "wait_for_sender", "wait_for_sender", before="_process_transit_recv")
        self.machine.add_transition("got_transit", "wait_for_sender_verify", "wait_for_sender_verify", before="_process_transit_recv")
        self.machine.add_transition("got_transit", "sender_connected", "sender_connected", before="_process_transit_recv")
        self.machine.add_transition("got_unverified_key", "wait_for_sender", "wait_for_sender_verify")
        self.machine.add_transition("got_verifier", "wait_for_sender_verify", "sender_connected", before="_got_verifier")
        self.machine.add_transition("got_message_offer", "sender_connected", "idle", after="_process_message_offer")
        self.machine.add_transition("got_file_offer", "sender_connected", "downloading", after="_process_file_offer")
        self.machine.add_transition("fail_download", "downloading", "idle", after="_download_failure")
        self.machine.add_transition("complete_download", "downloading", "idle", after="_download_success")

    def _on_error_before(self, desc=None):
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = True
        msg = "Logic error in state %s" % self.state
        if desc is not None:
            msg += "\nDescription: " + str(desc)
        self.tmp_error["message"] = msg
        if has_graph_capab:
            self.tmp_error["graph"] = self.machine.get_combined_graph()

    def _on_error_after(self, desc=None):
        status = self.app.orchestrator_error(self.tmp_error["message"])
        if status == QMessageBox.Help:
            self.visual_debug()
        elif status == QMessageBox.Retry:
            self.stargate.stop_all()
            self.rearm()
        self.tmp_error = {}

    def _on_rearm(self):
        self.stats.reset()

    def _on_wormhole_error(self, message):
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = True
        self.app.wormhole_error("Wormhole error in state %s:\n%s" % (self.state, str(message)))

    def _perform_connection(self, dc=None):
        self.stargate.connect()
        self.stats.wormhole_connected = False

    def _finish_connection(self, welcome):
        self.stats.wormhole_connected = True
        self.app.update_wormhole_action_text()

    def _finish_disconnection(self):
        self.stats.wormhole_connected = False
        self.stats.code_locked = False
        self.stats.peer_connected = False
        self.stats.upload_running = False
        self.stats.download_running = False
        self.app.update_wormhole_action_text()

    def _save_tmp_code(self, code):
        self.stats.code_locked = False
        self.tmp_code = code

    def _finish_hot_connection(self, welcome):
        self.stats.wormhole_connected = True
        self.app.update_wormhole_action_text()
        self.stats.code_locked = False
        self.stargate.set_code(self.tmp_code)

    def _set_code(self, code):
        self.stats.code_locked = False
        self.stargate.set_code(code)

    def _got_bad_code(self, msg):
        self.app.wormhole_error("Wormhole error in state %s:\n%s" % (self.state, str(msg)))
        self.stats.code_locked = False

    def _set_code_again(self, code):
        self.stargate.disconnect()

    def _got_code(self, code):
        self.stats.code_locked = True
        self.app.got_secret_code(code)

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

    def _continue_up_transfer(self, verifier=None):
        self.stats.waiting_peer = False
        if self.transfer_mode == TransferMode.Text:
            self.continue_sending_message()
        elif self.transfer_mode == TransferMode.File:
            self.continue_sending_file()
        else:
            self.error(verifier)

    def _continue_msg_transfer(self, msg=None):
        self.stargate.send_message(self.tmp_text)
        self.stats.msgs_sent += 1
        self.stats.upload_running = True

    def _continue_file_transfer(self, fname=None):
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
        self.error(answer)

    def _process_file_answer(self, answer):
        if "file_ack" in answer:
            if answer["file_ack"] == "ok":
                self.stargate.finish_sending_file(self.tmp_filename, self.app.send_progress_callback)
                return
        self.error(answer)

    def _upload_failure(self):
        self.stats.code_locked = False
        self.stats.upload_running = False
        self.stats.peer_connected = False
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = True
        self.stats.send_errors += 1

    def _upload_success(self):
        self.stats.code_locked = False
        self.stats.last_transfer_ok = True
        self.stats.last_transfer_fail = False
        self.stats.upload_running = False
        self.stats.peer_connected = False

    def _recv_any(self, code=None):
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
        self.stats.code_locked = False
        self.stats.download_running = False
        self.stats.peer_connected = False
        self.stats.last_transfer_ok = False
        self.stats.last_transfer_fail = True
        self.stats.recv_errors += 1

    def _download_success(self):
        self.stats.code_locked = False
        self.stats.last_transfer_ok = True
        self.stats.last_transfer_fail = False
        self.stats.download_running = False
        self.stats.peer_connected = False

    def visual_debug(self, recreate=True):
        if not has_graph_capab:
            self.app.orchestrator_error("Graphing feature unavailable on Microsoft Windows")
            return
        if recreate:
            self.tmp_error["graph"] = self.machine.get_combined_graph()
        graph = self.tmp_error["graph"]
        if self.state != "error":
            graph.remove_node("error")
        graph.draw(self.debug_graph_path, prog="dot")
        open_file(self.debug_graph_path)
