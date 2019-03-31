import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile


if __name__ == "__main__":
    app = QApplication(sys.argv)

    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor

    file = QFile("mainwindow.ui")
    file.open(QFile.ReadOnly)
    loader = QUiLoader()
    mainwindow = loader.load(file)

    from app import WormholeGui

    wgui = WormholeGui(app, mainwindow)

    mainwindow.show()

    #sys.exit(app.exec_())
    reactor.run()

