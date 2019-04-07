

class Stats:

    def __init__(self, callback_updated=None):
        self.callback_updated = callback_updated
        self._msgs_sent = 0
        self._files_sent = 0
        self._msgs_acks = 0
        self._file_acks = 0
        self._recv_errors = 0
        self._wormhole_connected = False
        self._peer_connected = False
        self._waiting_peer = False
        self._code_locked = False
        self._download_running = False
        self._upload_running = False

    @property
    def msgs_sent(self):
        return self._msgs_sent

    @property
    def files_sent(self):
        return self._files_sent

    @property
    def msgs_acks(self):
        return self._msgs_acks

    @property
    def file_acks(self):
        return self._file_acks

    @property
    def recv_errors(self):
        return self._recv_errors

    @property
    def wormhole_connected(self):
        return self._wormhole_connected

    @property
    def peer_connected(self):
        return self._peer_connected

    @property
    def waiting_peer(self):
        return self._waiting_peer

    @property
    def code_locked(self):
        return self._code_locked

    @property
    def download_running(self):
        return self._download_running

    @property
    def upload_running(self):
        return self._upload_running

    @msgs_sent.setter
    def msgs_sent(self, value):
        self._msgs_sent = value
        if self.callback_updated is not None: self.callback_updated(self)

    @files_sent.setter
    def files_sent(self, value):
        self._files_sent = value
        if self.callback_updated is not None: self.callback_updated(self)

    @msgs_acks.setter
    def msgs_acks(self, value):
        self._msgs_acks = value
        if self.callback_updated is not None: self.callback_updated(self)

    @file_acks.setter
    def file_acks(self, value):
        self._file_acks = value
        if self.callback_updated is not None: self.callback_updated(self)

    @recv_errors.setter
    def recv_errors(self, value):
        self._recv_errors = value
        if self.callback_updated is not None: self.callback_updated(self)

    @wormhole_connected.setter
    def wormhole_connected(self, value):
        self._wormhole_connected = value
        if not self._wormhole_connected:
            self._peer_connected = False
            self._code_locked = False
            self._download_running = False
            self._upload_running = False
            self._waiting_peer = False
        if self.callback_updated is not None: self.callback_updated(self)

    @peer_connected.setter
    def peer_connected(self, value):
        if value and not self._peer_connected:
            self._code_locked = False

        if self._peer_connected:
            self._waiting_peer = False

        self._peer_connected = value
        if self.callback_updated is not None: self.callback_updated(self)

    @waiting_peer.setter
    def waiting_peer(self, value):
        self._waiting_peer = value
        if self.callback_updated is not None: self.callback_updated(self)

    @code_locked.setter
    def code_locked(self, value):
        self._code_locked = value
        if self.callback_updated is not None: self.callback_updated(self)

    @download_running.setter
    def download_running(self, value):
        self._download_running = value
        if self.callback_updated is not None: self.callback_updated(self)

    @upload_running.setter
    def upload_running(self, value):
        self._upload_running = value
        if self.callback_updated is not None: self.callback_updated(self)




