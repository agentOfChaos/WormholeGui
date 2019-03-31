

class Stats:

    def __init__(self, callback_updated=None):
        self.callback_updated = callback_updated
        self._msgs_sent = 0
        self._files_sent = 0
        self._msgs_acks = 0
        self._file_acks = 0
        self._recv_errors = 0

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








