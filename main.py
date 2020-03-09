#!/usr/bin/env python3

import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile

from twisted.internet.error import ReactorAlreadyInstalledError


from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == "__main__":
    qtapp = QApplication(sys.argv)

    import qt5reactor

    try:
        qt5reactor.install()
    except ReactorAlreadyInstalledError:
        pass

    from twisted.internet import reactor

    #file = QFile("mainwindow.ui")
    #file.open(QFile.ReadOnly)
    #loader = QUiLoader()
    #mainwindow = loader.load(file)

    mainwindow = MainWindow()

    from app import WormholeGui

    wgui = WormholeGui(qtapp, mainwindow)

    mainwindow.show()

    #sys.exit(app.exec_())
    reactor.run()

