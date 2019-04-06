from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import Qt, QEvent


class TabCompleteQLineEdit(QLineEdit):

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.setFocus()
            possibilities = self.completer().model().stringList()
            if len(possibilities) > 0:
                self.setText(possibilities[0])
            return False
        return QLineEdit.event(self, event)
