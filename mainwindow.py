# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

from custom_ui.TabCompleteQLineEdit import TabCompleteQLineEdit
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(787, 842)
        self.actionWormhole = QAction(MainWindow)
        self.actionWormhole.setObjectName(u"actionWormhole")
        self.actionOpenFile = QAction(MainWindow)
        self.actionOpenFile.setObjectName(u"actionOpenFile")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionViewGraph = QAction(MainWindow)
        self.actionViewGraph.setObjectName(u"actionViewGraph")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setIconSize(QSize(32, 32))
        self.tabTransmit = QWidget()
        self.tabTransmit.setObjectName(u"tabTransmit")
        self.gridLayout_8 = QGridLayout(self.tabTransmit)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticalWidget = QWidget(self.tabTransmit)
        self.verticalWidget.setObjectName(u"verticalWidget")
        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.frame = QFrame(self.verticalWidget)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.txtSecretCode = QLineEdit(self.frame)
        self.txtSecretCode.setObjectName(u"txtSecretCode")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.txtSecretCode.sizePolicy().hasHeightForWidth())
        self.txtSecretCode.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(14)
        self.txtSecretCode.setFont(font)
        self.txtSecretCode.setReadOnly(False)
        self.txtSecretCode.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.txtSecretCode, 1, 1, 1, 1)

        self.btnCopyCode = QPushButton(self.frame)
        self.btnCopyCode.setObjectName(u"btnCopyCode")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btnCopyCode.sizePolicy().hasHeightForWidth())
        self.btnCopyCode.setSizePolicy(sizePolicy3)
        icon = QIcon()
        icon.addFile(u":/newPrefix/icons/edit-copy-6.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnCopyCode.setIcon(icon)

        self.gridLayout_13.addWidget(self.btnCopyCode, 1, 4, 1, 1)

        self.btnSetCode = QPushButton(self.frame)
        self.btnSetCode.setObjectName(u"btnSetCode")
        sizePolicy3.setHeightForWidth(self.btnSetCode.sizePolicy().hasHeightForWidth())
        self.btnSetCode.setSizePolicy(sizePolicy3)
        icon1 = QIcon()
        icon1.addFile(u":/newPrefix/icons/lock-silver.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSetCode.setIcon(icon1)
        self.btnSetCode.setIconSize(QSize(32, 32))

        self.gridLayout_13.addWidget(self.btnSetCode, 1, 3, 1, 1)

        self.btnGenerateCode = QPushButton(self.frame)
        self.btnGenerateCode.setObjectName(u"btnGenerateCode")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(2)
        sizePolicy4.setHeightForWidth(self.btnGenerateCode.sizePolicy().hasHeightForWidth())
        self.btnGenerateCode.setSizePolicy(sizePolicy4)
        icon2 = QIcon()
        icon2.addFile(u":/newPrefix/icons/roll-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnGenerateCode.setIcon(icon2)
        self.btnGenerateCode.setIconSize(QSize(32, 32))

        self.gridLayout_13.addWidget(self.btnGenerateCode, 1, 0, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy5)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75);
        self.label_3.setFont(font1)
        self.label_3.setStyleSheet(u"")

        self.gridLayout_13.addWidget(self.label_3, 0, 0, 1, 3)


        self.verticalLayout.addWidget(self.frame)

        self.widget_2 = QWidget(self.verticalWidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(7)
        sizePolicy6.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy6)
        self.gridLayout_9 = QGridLayout(self.widget_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_3 = QFrame(self.widget_2)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy7)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_3)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(6, -1, -1, -1)
        self.btnBrowseFile = QPushButton(self.frame_3)
        self.btnBrowseFile.setObjectName(u"btnBrowseFile")

        self.gridLayout_12.addWidget(self.btnBrowseFile, 6, 0, 1, 1)

        self.txtFileName = QLineEdit(self.frame_3)
        self.txtFileName.setObjectName(u"txtFileName")

        self.gridLayout_12.addWidget(self.txtFileName, 4, 0, 2, 4)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_3, 8, 0, 1, 1)

        self.label_9 = QLabel(self.frame_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_12.addWidget(self.label_9, 9, 0, 1, 1)

        self.label_8 = QLabel(self.frame_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_12.addWidget(self.label_8, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.progressSendFile = QProgressBar(self.frame_3)
        self.progressSendFile.setObjectName(u"progressSendFile")
        self.progressSendFile.setValue(0)

        self.gridLayout_12.addWidget(self.progressSendFile, 10, 0, 1, 4)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 13, 0, 1, 1)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.gridLayout_12.addWidget(self.label_4, 0, 0, 1, 1)

        self.btnSendFile = QPushButton(self.frame_3)
        self.btnSendFile.setObjectName(u"btnSendFile")

        self.gridLayout_12.addWidget(self.btnSendFile, 11, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_3, 11, 1, 1, 3)

        self.widget_6 = QWidget(self.frame_3)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lblSendTotal = QLabel(self.widget_6)
        self.lblSendTotal.setObjectName(u"lblSendTotal")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.lblSendTotal.sizePolicy().hasHeightForWidth())
        self.lblSendTotal.setSizePolicy(sizePolicy8)

        self.horizontalLayout_5.addWidget(self.lblSendTotal)

        self.lblSendRate = QLabel(self.widget_6)
        self.lblSendRate.setObjectName(u"lblSendRate")
        sizePolicy8.setHeightForWidth(self.lblSendRate.sizePolicy().hasHeightForWidth())
        self.lblSendRate.setSizePolicy(sizePolicy8)
        self.lblSendRate.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.lblSendRate)

        self.lblSendETA = QLabel(self.widget_6)
        self.lblSendETA.setObjectName(u"lblSendETA")
        sizePolicy8.setHeightForWidth(self.lblSendETA.sizePolicy().hasHeightForWidth())
        self.lblSendETA.setSizePolicy(sizePolicy8)
        self.lblSendETA.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.lblSendETA)


        self.gridLayout_12.addWidget(self.widget_6, 12, 0, 1, 4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_2, 6, 1, 1, 3)


        self.horizontalLayout.addWidget(self.frame_3)

        self.frame_2 = QFrame(self.widget_2)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy7.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy7)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.gridLayout_10.addWidget(self.label_5, 0, 0, 1, 1)

        self.btnSendMsg = QPushButton(self.frame_2)
        self.btnSendMsg.setObjectName(u"btnSendMsg")
        sizePolicy9 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(1)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.btnSendMsg.sizePolicy().hasHeightForWidth())
        self.btnSendMsg.setSizePolicy(sizePolicy9)

        self.gridLayout_10.addWidget(self.btnSendMsg, 2, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer, 2, 1, 1, 1)

        self.txtMessage = QPlainTextEdit(self.frame_2)
        self.txtMessage.setObjectName(u"txtMessage")

        self.gridLayout_10.addWidget(self.txtMessage, 1, 0, 1, 2)


        self.horizontalLayout.addWidget(self.frame_2)


        self.gridLayout_9.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.widget_2)


        self.gridLayout_8.addWidget(self.verticalWidget, 0, 0, 1, 1)

        icon3 = QIcon()
        icon3.addFile(u":/newPrefix/icons/mail-outbox.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tabTransmit, icon3, "")
        self.tabReceive = QWidget()
        self.tabReceive.setObjectName(u"tabReceive")
        self.gridLayout_15 = QGridLayout(self.tabReceive)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.widget_4 = QWidget(self.tabReceive)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_2 = QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(7)
        sizePolicy10.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy10)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.frame_5 = QFrame(self.widget_5)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy7.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy7)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_5)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(-1, -1, 6, -1)
        self.txtFolderName = QLineEdit(self.frame_5)
        self.txtFolderName.setObjectName(u"txtFolderName")

        self.gridLayout_16.addWidget(self.txtFolderName, 4, 0, 2, 4)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_16.addItem(self.verticalSpacer_5, 1, 0, 1, 4)

        self.btnBrowseFolder = QPushButton(self.frame_5)
        self.btnBrowseFolder.setObjectName(u"btnBrowseFolder")
        self.btnBrowseFolder.setMinimumSize(QSize(0, 0))
        self.btnBrowseFolder.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_16.addWidget(self.btnBrowseFolder, 6, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_16.addItem(self.verticalSpacer_4, 7, 0, 1, 4)

        self.progressRecvFile = QProgressBar(self.frame_5)
        self.progressRecvFile.setObjectName(u"progressRecvFile")
        self.progressRecvFile.setValue(0)

        self.gridLayout_16.addWidget(self.progressRecvFile, 14, 0, 1, 4)

        self.label_16 = QLabel(self.frame_5)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_16.addWidget(self.label_16, 8, 0, 1, 4)

        self.label_17 = QLabel(self.frame_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_17, 9, 0, 1, 1)

        self.label_18 = QLabel(self.frame_5)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_18, 11, 0, 1, 1)

        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.gridLayout_16.addWidget(self.label_11, 0, 0, 1, 4)

        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_16.addWidget(self.label_12, 13, 0, 1, 4)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_16.addItem(self.verticalSpacer_6, 12, 0, 1, 4)

        self.label_13 = QLabel(self.frame_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_16.addWidget(self.label_13, 2, 0, 1, 4)

        self.lblRecvFileName = QLabel(self.frame_5)
        self.lblRecvFileName.setObjectName(u"lblRecvFileName")

        self.gridLayout_16.addWidget(self.lblRecvFileName, 9, 2, 1, 1)

        self.widget_3 = QWidget(self.frame_5)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetMaximumSize)
        self.lblRecvTotal = QLabel(self.widget_3)
        self.lblRecvTotal.setObjectName(u"lblRecvTotal")
        sizePolicy8.setHeightForWidth(self.lblRecvTotal.sizePolicy().hasHeightForWidth())
        self.lblRecvTotal.setSizePolicy(sizePolicy8)
        self.lblRecvTotal.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_4.addWidget(self.lblRecvTotal)

        self.lblRecvRate = QLabel(self.widget_3)
        self.lblRecvRate.setObjectName(u"lblRecvRate")
        sizePolicy8.setHeightForWidth(self.lblRecvRate.sizePolicy().hasHeightForWidth())
        self.lblRecvRate.setSizePolicy(sizePolicy8)
        self.lblRecvRate.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.lblRecvRate)

        self.lblRecvETA = QLabel(self.widget_3)
        self.lblRecvETA.setObjectName(u"lblRecvETA")
        sizePolicy8.setHeightForWidth(self.lblRecvETA.sizePolicy().hasHeightForWidth())
        self.lblRecvETA.setSizePolicy(sizePolicy8)
        self.lblRecvETA.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.lblRecvETA)


        self.gridLayout_16.addWidget(self.widget_3, 15, 0, 1, 4)

        self.lcdNumber = QLCDNumber(self.frame_5)
        self.lcdNumber.setObjectName(u"lcdNumber")
        sizePolicy11 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy11)
        self.lcdNumber.setSmallDecimalPoint(True)
        self.lcdNumber.setDigitCount(15)
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setProperty("value", 0.000000000000000)
        self.lcdNumber.setProperty("intValue", 0)

        self.gridLayout_16.addWidget(self.lcdNumber, 11, 1, 1, 3)


        self.horizontalLayout_3.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.widget_5)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy7.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy7)
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_6)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.btnClearRecvMsg = QPushButton(self.frame_6)
        self.btnClearRecvMsg.setObjectName(u"btnClearRecvMsg")

        self.gridLayout_17.addWidget(self.btnClearRecvMsg, 2, 0, 1, 1)

        self.txtMessageRecv = QPlainTextEdit(self.frame_6)
        self.txtMessageRecv.setObjectName(u"txtMessageRecv")
        self.txtMessageRecv.setReadOnly(True)

        self.gridLayout_17.addWidget(self.txtMessageRecv, 1, 0, 1, 3)

        self.chkAppend = QCheckBox(self.frame_6)
        self.chkAppend.setObjectName(u"chkAppend")
        self.chkAppend.setChecked(True)

        self.gridLayout_17.addWidget(self.chkAppend, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_4, 2, 1, 1, 1)

        self.label_15 = QLabel(self.frame_6)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font1)

        self.gridLayout_17.addWidget(self.label_15, 0, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.frame_6)


        self.verticalLayout_2.addWidget(self.widget_5)

        self.frame_4 = QFrame(self.widget_4)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy1.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy1)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_4)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(6, -1, -1, -1)
        self.txtSecretCodeRecv = TabCompleteQLineEdit(self.frame_4)
        self.txtSecretCodeRecv.setObjectName(u"txtSecretCodeRecv")
        sizePolicy2.setHeightForWidth(self.txtSecretCodeRecv.sizePolicy().hasHeightForWidth())
        self.txtSecretCodeRecv.setSizePolicy(sizePolicy2)
        self.txtSecretCodeRecv.setFont(font)
        self.txtSecretCodeRecv.setFocusPolicy(Qt.StrongFocus)
        self.txtSecretCodeRecv.setReadOnly(False)
        self.txtSecretCodeRecv.setClearButtonEnabled(True)

        self.gridLayout_14.addWidget(self.txtSecretCodeRecv, 1, 0, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        sizePolicy5.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy5)
        self.label_10.setFont(font1)
        self.label_10.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.label_10, 0, 0, 1, 1)

        self.btnPasteCode = QPushButton(self.frame_4)
        self.btnPasteCode.setObjectName(u"btnPasteCode")
        sizePolicy3.setHeightForWidth(self.btnPasteCode.sizePolicy().hasHeightForWidth())
        self.btnPasteCode.setSizePolicy(sizePolicy3)
        icon4 = QIcon()
        icon4.addFile(u":/newPrefix/icons/edit-paste-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnPasteCode.setIcon(icon4)

        self.gridLayout_14.addWidget(self.btnPasteCode, 1, 2, 1, 1)

        self.btnSetCodeRecv = QPushButton(self.frame_4)
        self.btnSetCodeRecv.setObjectName(u"btnSetCodeRecv")
        sizePolicy3.setHeightForWidth(self.btnSetCodeRecv.sizePolicy().hasHeightForWidth())
        self.btnSetCodeRecv.setSizePolicy(sizePolicy3)
        icon5 = QIcon()
        icon5.addFile(u":/newPrefix/icons/lock-6.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSetCodeRecv.setIcon(icon5)
        self.btnSetCodeRecv.setIconSize(QSize(32, 32))

        self.gridLayout_14.addWidget(self.btnSetCodeRecv, 1, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_4)


        self.gridLayout_15.addWidget(self.widget_4, 1, 0, 1, 1)

        icon6 = QIcon()
        icon6.addFile(u":/newPrefix/icons/mail-receive.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tabReceive, icon6, "")
        self.tabSettings = QWidget()
        self.tabSettings.setObjectName(u"tabSettings")
        self.gridLayout_3 = QGridLayout(self.tabSettings)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.widget_1 = QWidget(self.tabSettings)
        self.widget_1.setObjectName(u"widget_1")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.widget_1.sizePolicy().hasHeightForWidth())
        self.widget_1.setSizePolicy(sizePolicy12)
        self.gridLayout = QGridLayout(self.widget_1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnSaveSetup = QPushButton(self.widget_1)
        self.btnSaveSetup.setObjectName(u"btnSaveSetup")
        sizePolicy13 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.btnSaveSetup.sizePolicy().hasHeightForWidth())
        self.btnSaveSetup.setSizePolicy(sizePolicy13)
        self.btnSaveSetup.setMinimumSize(QSize(250, 0))

        self.gridLayout.addWidget(self.btnSaveSetup, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.widget_1, 1, 0, 1, 1)

        self.widget_7 = QWidget(self.tabSettings)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy14 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy14)
        self.formLayout = QFormLayout(self.widget_7)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setContentsMargins(100, -1, 100, -1)
        self.label = QLabel(self.widget_7)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.txtRelay = QLineEdit(self.widget_7)
        self.txtRelay.setObjectName(u"txtRelay")
        sizePolicy15 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.txtRelay.sizePolicy().hasHeightForWidth())
        self.txtRelay.setSizePolicy(sizePolicy15)
        self.txtRelay.setText(u"")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txtRelay)

        self.label_7 = QLabel(self.widget_7)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.txtTransit = QLineEdit(self.widget_7)
        self.txtTransit.setObjectName(u"txtTransit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.txtTransit)

        self.label_2 = QLabel(self.widget_7)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.txtAppID = QLineEdit(self.widget_7)
        self.txtAppID.setObjectName(u"txtAppID")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.txtAppID)

        self.label_6 = QLabel(self.widget_7)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.cmbLanguage = QComboBox(self.widget_7)
        self.cmbLanguage.addItem("")
        self.cmbLanguage.setObjectName(u"cmbLanguage")
        sizePolicy13.setHeightForWidth(self.cmbLanguage.sizePolicy().hasHeightForWidth())
        self.cmbLanguage.setSizePolicy(sizePolicy13)
        self.cmbLanguage.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.cmbLanguage)


        self.gridLayout_7.addWidget(self.widget_7, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        icon7 = QIcon()
        icon7.addFile(u":/newPrefix/icons/preferences-system-4.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tabSettings, icon7, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_11 = QGridLayout(self.tab)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.txtLog = QPlainTextEdit(self.tab)
        self.txtLog.setObjectName(u"txtLog")
        self.txtLog.setReadOnly(True)

        self.gridLayout_11.addWidget(self.txtLog, 0, 0, 1, 1)

        icon8 = QIcon()
        icon8.addFile(u":/newPrefix/icons/utilities-log_viewer.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab, icon8, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.frame_8 = QFrame(self.centralwidget)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_14 = QLabel(self.frame_8)
        self.label_14.setObjectName(u"label_14")
        sizePolicy5.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy5)
        self.label_14.setFont(font1)
        self.label_14.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.label_14)

        self.txtPeerAddress = QTextBrowser(self.frame_8)
        self.txtPeerAddress.setObjectName(u"txtPeerAddress")
        sizePolicy11.setHeightForWidth(self.txtPeerAddress.sizePolicy().hasHeightForWidth())
        self.txtPeerAddress.setSizePolicy(sizePolicy11)
        self.txtPeerAddress.setMaximumSize(QSize(16777215, 35))
        font2 = QFont()
        font2.setPointSize(12)
        self.txtPeerAddress.setFont(font2)
        self.txtPeerAddress.setLineWrapMode(QTextEdit.NoWrap)

        self.horizontalLayout_6.addWidget(self.txtPeerAddress)


        self.verticalLayout_3.addWidget(self.frame_8)

        self.frame_7 = QFrame(self.centralwidget)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy16 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy16)
        self.frame_7.setMinimumSize(QSize(0, 0))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lblHasWormhole = QLabel(self.frame_7)
        self.lblHasWormhole.setObjectName(u"lblHasWormhole")
        self.lblHasWormhole.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.lblHasWormhole)

        self.lblHasCode = QLabel(self.frame_7)
        self.lblHasCode.setObjectName(u"lblHasCode")
        sizePolicy17 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy17.setHorizontalStretch(0)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.lblHasCode.sizePolicy().hasHeightForWidth())
        self.lblHasCode.setSizePolicy(sizePolicy17)

        self.horizontalLayout_2.addWidget(self.lblHasCode)

        self.lblHasWait = QLabel(self.frame_7)
        self.lblHasWait.setObjectName(u"lblHasWait")

        self.horizontalLayout_2.addWidget(self.lblHasWait)

        self.lblHasPeer = QLabel(self.frame_7)
        self.lblHasPeer.setObjectName(u"lblHasPeer")

        self.horizontalLayout_2.addWidget(self.lblHasPeer)

        self.lblHasDownload = QLabel(self.frame_7)
        self.lblHasDownload.setObjectName(u"lblHasDownload")

        self.horizontalLayout_2.addWidget(self.lblHasDownload)

        self.lblHasUpload = QLabel(self.frame_7)
        self.lblHasUpload.setObjectName(u"lblHasUpload")

        self.horizontalLayout_2.addWidget(self.lblHasUpload)

        self.lblHasSuccess = QLabel(self.frame_7)
        self.lblHasSuccess.setObjectName(u"lblHasSuccess")

        self.horizontalLayout_2.addWidget(self.lblHasSuccess)

        self.lblHasFailure = QLabel(self.frame_7)
        self.lblHasFailure.setObjectName(u"lblHasFailure")

        self.horizontalLayout_2.addWidget(self.lblHasFailure)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.btnStop = QPushButton(self.frame_7)
        self.btnStop.setObjectName(u"btnStop")
        sizePolicy13.setHeightForWidth(self.btnStop.sizePolicy().hasHeightForWidth())
        self.btnStop.setSizePolicy(sizePolicy13)
        icon9 = QIcon()
        icon9.addFile(u":/newPrefix/icons/process-stop.png", QSize(), QIcon.Normal, QIcon.On)
        self.btnStop.setIcon(icon9)
        self.btnStop.setIconSize(QSize(64, 64))
        self.btnStop.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btnStop)


        self.verticalLayout_3.addWidget(self.frame_7)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 787, 25))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuDebug = QMenu(self.menubar)
        self.menuDebug.setObjectName(u"menuDebug")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDebug.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionWormhole)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuDebug.addAction(self.actionViewGraph)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionWormhole.setText(QCoreApplication.translate("MainWindow", u"Connetti wormhole", None))
        self.actionOpenFile.setText(QCoreApplication.translate("MainWindow", u"Seleziona file...", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Esci", None))
        self.actionViewGraph.setText(QCoreApplication.translate("MainWindow", u"Grafico stato...", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About...", None))
        self.txtSecretCode.setText("")
        self.btnCopyCode.setText(QCoreApplication.translate("MainWindow", u"Copia", None))
        self.btnSetCode.setText(QCoreApplication.translate("MainWindow", u"Conferma\n"
"Codice", None))
        self.btnGenerateCode.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Codice segreto", None))
        self.btnBrowseFile.setText(QCoreApplication.translate("MainWindow", u"sfoglia", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Trasferimento", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Selezione file", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Invia un file", None))
        self.btnSendFile.setText(QCoreApplication.translate("MainWindow", u"Invia", None))
        self.lblSendTotal.setText("")
        self.lblSendRate.setText("")
        self.lblSendETA.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Invia un messaggio", None))
        self.btnSendMsg.setText(QCoreApplication.translate("MainWindow", u"Invia", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTransmit), QCoreApplication.translate("MainWindow", u"Invia", None))
        self.btnBrowseFolder.setText(QCoreApplication.translate("MainWindow", u"sfoglia", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Dettagli File:", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Nome:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Dimensioni (bytes):", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Ricezione file", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Trasferimento", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Directory destinazione:", None))
        self.lblRecvFileName.setText("")
        self.lblRecvTotal.setText("")
        self.lblRecvRate.setText("")
        self.lblRecvETA.setText("")
        self.btnClearRecvMsg.setText(QCoreApplication.translate("MainWindow", u"Svuota", None))
        self.chkAppend.setText(QCoreApplication.translate("MainWindow", u"Appendi", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Ricezione testo", None))
        self.txtSecretCodeRecv.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Codice segreto", None))
        self.btnPasteCode.setText(QCoreApplication.translate("MainWindow", u"Incolla", None))
        self.btnSetCodeRecv.setText(QCoreApplication.translate("MainWindow", u"Conferma\n"
"Trasferimento", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabReceive), QCoreApplication.translate("MainWindow", u"Ricevi", None))
        self.btnSaveSetup.setText(QCoreApplication.translate("MainWindow", u"Salva", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Rendez-Vous relay:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Transit relay:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"App ID:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Lingua:", None))
        self.cmbLanguage.setItemText(0, QCoreApplication.translate("MainWindow", u"Default sistema", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings), QCoreApplication.translate("MainWindow", u"Setup", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Logging", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Connesso a:", None))
        self.txtPeerAddress.setMarkdown("")
#if QT_CONFIG(tooltip)
        self.lblHasWormhole.setToolTip(QCoreApplication.translate("MainWindow", u"Wormhole connected", None))
#endif // QT_CONFIG(tooltip)
        self.lblHasWormhole.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/newPrefix/icons/network-globe.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lblHasCode.setToolTip(QCoreApplication.translate("MainWindow", u"Secret code locked", None))
#endif // QT_CONFIG(tooltip)
        self.lblHasCode.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/newPrefix/icons/application-x-octet-stream.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lblHasWait.setToolTip(QCoreApplication.translate("MainWindow", u"Waiting for peer", None))
#endif // QT_CONFIG(tooltip)
        self.lblHasWait.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/newPrefix/icons/hourglass-2.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lblHasPeer.setToolTip(QCoreApplication.translate("MainWindow", u"Peer connected", None))
#endif // QT_CONFIG(tooltip)
        self.lblHasPeer.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/newPrefix/icons/user-group-new-2.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lblHasDownload.setToolTip(QCoreApplication.translate("MainWindow", u"Download in progress", None))
#endif // QT_CONFIG(tooltip)
        self.lblHasDownload.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/newPrefix/icons/download.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lblHasUpload.setToolTip(QCoreApplication.translate("MainWindow", u"Upload in progress", None))
#endif // QT_CONFIG(tooltip)
        self.lblHasUpload.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/newPrefix/icons/mail-send.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lblHasSuccess.setToolTip(QCoreApplication.translate("MainWindow", u"Transfer succesful", None))
#endif // QT_CONFIG(tooltip)
        self.lblHasSuccess.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/newPrefix/icons/dialog-ok-apply-6.png\"/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lblHasFailure.setToolTip(QCoreApplication.translate("MainWindow", u"Transfer failure", None))
#endif // QT_CONFIG(tooltip)
        self.lblHasFailure.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/newPrefix/icons/dialog-cancel-2.png\"/></p></body></html>", None))
        self.btnStop.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuDebug.setTitle(QCoreApplication.translate("MainWindow", u"Debug", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

