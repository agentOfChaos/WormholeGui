import setup
import configparser
import appdirs
import os
import sys
import logging
import secrets
from logging import StreamHandler
from PySide2.QtCore import QEvent, QObject, QTranslator, QLocale, QStringListModel
from PySide2.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QApplication, QCompleter
from PySide2.QtGui import QTextCursor, QGuiApplication
from langcodes import Language


from progress import CustomProgressIndicator
from stargate import StarGate
from stats import Stats
from utils import has_error_message, init_label_opacity
from wormhole.errors import KeyFormatError
from wormhole._wordlist import raw_words as pgp_words


class CustomLogHandler(StreamHandler):

    def __init__(self, textbox):
        super(StreamHandler, self).__init__()
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.moveCursor(QTextCursor.End)
        self.textbox.insertPlainText(msg + "\n")
        self.textbox.moveCursor(QTextCursor.End)

    def flush(self):
        pass


class WormholeGui(QObject):

    appname = "WormholeGui"
    appauthor = "WormholeGui"

    translation_folder = "i18n"
    wordlist_folder = "wordlist"

    opacity_off = 0.15


    def __init__(self, app: QApplication, mainwindow: QMainWindow):
        super(WormholeGui, self).__init__()
        self.app = app
        self.mainwindow = mainwindow
        self.progress_counter = None
        self.opacity_filters = {}
        self.available_languages = []
        self.code_wordlist = []
        self.num_codewords = 3
        self.setup_logger(logging.DEBUG)

        self.config = configparser.ConfigParser()

        self.stats = Stats(callback_updated=self.show_stats)
        self.stargate = StarGate(self.config, self.stats, self.logger, self.got_secret_code)
        self.load_config()

        self.setup_translator()
        self.setup_controls()
        self.show_config()
        self.show_stats(self.stats)

    @property
    def config_filename(self):
        return os.path.join(appdirs.user_config_dir(self.appname, self.appauthor), "config.ini")

    def setup_logger(self, loglevel):
        self.loglevel = loglevel
        self.logger = logging.getLogger(self.appname)
        self.logger.setLevel(loglevel)
        self.logger.handlers = []

        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s: [%(name)s][%(levelname)s]: %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        txt = CustomLogHandler(self.mainwindow.txtLog)
        txt.setFormatter(formatter)
        self.logger.addHandler(txt)

    def setup_translator(self):
        self.translator = QTranslator()
        language_code = self.config["app"]["language"]
        if language_code == "systemdefault":
            language_code = QLocale.system().name()
        translation_filename = os.path.join(self.translation_folder, "%s.qm" % language_code)
        if self.translator.load(translation_filename):
            self.logger.debug("Loaded %s translation." % language_code)
        else:
            self.logger.warning("Translation file %s not found." % translation_filename)
        self.app.installTranslator(self.translator)
        self.mainwindow.retranslateUi(self.mainwindow)
        self.available_languages = ["systemdefault"] + list(map(lambda fname: fname[:-3],
                                                                filter(lambda fname: fname.endswith(".qm"),
                                                                       os.listdir(self.translation_folder))))
        self.code_wordlist = []
        for bite, pair in pgp_words.items():
            self.code_wordlist.extend(pair)

        wordlist_filename = os.path.join(self.wordlist_folder, "%s.txt" % language_code)
        if os.path.isfile(wordlist_filename):
            with open(wordlist_filename, "r") as fp:
                self.code_wordlist = list(filter(lambda i: len(i.strip()) > 0,
                                                 fp.read().split("\n")))
            self.logger.debug("Loaded %s wordlist." % wordlist_filename)
        else:
            self.logger.warning("Wordlist file %s not found." % wordlist_filename)


    def setup_controls(self):
        init_label_opacity(self, self.mainwindow.lblHasWormhole, self.opacity_off)
        init_label_opacity(self, self.mainwindow.lblHasCode, self.opacity_off)
        init_label_opacity(self, self.mainwindow.lblHasPeer, self.opacity_off)
        init_label_opacity(self, self.mainwindow.lblHasDownload, self.opacity_off)
        init_label_opacity(self, self.mainwindow.lblHasUpload, self.opacity_off)
        init_label_opacity(self, self.mainwindow.lblHasWait, self.opacity_off)
        init_label_opacity(self, self.mainwindow.lblHasSuccess, self.opacity_off)
        init_label_opacity(self, self.mainwindow.lblHasFailure, self.opacity_off)

        self.mainwindow.installEventFilter(self)
        self.mainwindow.btnSaveSetup.clicked.connect(self.save_settings)
        self.mainwindow.btnGenerateCode.clicked.connect(self.allocate_code)
        self.mainwindow.btnSetCode.clicked.connect(self.set_code)
        self.mainwindow.btnSendMsg.clicked.connect(self.send_text)
        self.mainwindow.btnBrowseFile.clicked.connect(self.browse_file)
        self.mainwindow.btnBrowseFolder.clicked.connect(self.browse_folder)
        self.mainwindow.btnSendFile.clicked.connect(self.send_file)
        self.mainwindow.btnCopyCode.clicked.connect(self.copy_secret_code)
        self.mainwindow.btnPasteCode.clicked.connect(self.paste_secret_code)
        self.mainwindow.btnSetCodeRecv.clicked.connect(self.recv_anything)
        self.mainwindow.btnClearRecvMsg.clicked.connect(self.clear_received_text)
        self.mainwindow.btnStop.clicked.connect(self.super_stop)

        self.mainwindow.actionWormhole.triggered.connect(self.toggle_connect_wormhole)
        self.mainwindow.actionOpenFile.triggered.connect(self.browse_file)
        self.mainwindow.actionQuit.triggered.connect(self.on_exit)

        self.mainwindow.cmbLanguage.addItems(list(map(lambda langcode: Language.get(langcode).autonym(),
                                                      self.available_languages[1:])))

        self.mainwindow.txtSecretCodeRecv.textEdited.connect(self.suggest_code)
        completer = QCompleter()
        model = QStringListModel()
        completer.setModel(model)
        self.mainwindow.txtSecretCodeRecv.setCompleter(completer)

    def eventFilter(self, obj, event):
        if obj is self.mainwindow and event.type() == QEvent.Close:
            self.on_exit()
            event.ignore()
            return True
        return super(WormholeGui, self).eventFilter(obj, event)

    def on_exit(self):
        self.logger.debug("Quitting the application")
        self.mainwindow.removeEventFilter(self)
        self.app.quit()


    def load_config(self):
        self.config.read(self.config_filename)
        self.stargate.config = self.config
        setup.default_config_params(self.config)
        if not os.path.isfile(self.config_filename):
            os.makedirs(os.path.dirname(self.config_filename), exist_ok=True)
            with open(self.config_filename, "w") as fp:
                self.config.write(fp)

    def show_config(self):
        self.mainwindow.txtRelay.setText(self.config["wormhole"]["relay"])
        self.mainwindow.txtAppID.setText(self.config["wormhole"]["appid"])
        self.mainwindow.txtTransit.setText(self.config["wormhole"]["transit"])
        self.mainwindow.txtFolderName.setText(self.config["app"]["download_folder"])

        langcode = self.config["app"]["language"]
        if langcode == "systemdefault":
            self.mainwindow.cmbLanguage.setCurrentIndex(0)
        else:
            allitems = [self.mainwindow.cmbLanguage.itemText(i) for i in range(self.mainwindow.cmbLanguage.count())]
            try:
                langindex = allitems.index(Language.get(langcode).autonym())
                self.mainwindow.cmbLanguage.setCurrentIndex(langindex)
            except ValueError:
                self.mainwindow.cmbLanguage.setCurrentIndex(0)

    @has_error_message
    def save_settings(self):
        self.config["wormhole"]["relay"] = self.mainwindow.txtRelay.text()
        self.config["wormhole"]["appid"] = self.mainwindow.txtAppID.text()
        self.config["wormhole"]["transit"] = self.mainwindow.txtTransit.text()
        self.config["app"]["download_folder"] = self.mainwindow.txtFolderName.text()
        self.config["app"]["language"] = self.available_languages[self.mainwindow.cmbLanguage.currentIndex()]

        with open(self.config_filename, "w") as fp:
            self.config.write(fp)
        self.mainwindow.statusbar.showMessage(self.translator.translate("StatusMessage", "Settings saved!"), 5000)

    def show_stats(self, stats: Stats):
        try:
            self.opacity_filters[self.mainwindow.lblHasWormhole].setOpacity(1.0 if stats.wormhole_connected else self.opacity_off)
            self.opacity_filters[self.mainwindow.lblHasCode].setOpacity(1.0 if stats.code_locked else self.opacity_off)
            self.opacity_filters[self.mainwindow.lblHasPeer].setOpacity(1.0 if stats.peer_connected else self.opacity_off)
            self.opacity_filters[self.mainwindow.lblHasDownload].setOpacity(1.0 if stats.download_running else self.opacity_off)
            self.opacity_filters[self.mainwindow.lblHasUpload].setOpacity(1.0 if stats.upload_running else self.opacity_off)
            self.opacity_filters[self.mainwindow.lblHasWait].setOpacity(1.0 if stats.waiting_peer else self.opacity_off)
            self.opacity_filters[self.mainwindow.lblHasFailure].setOpacity(1.0 if stats.last_transfer_fail else self.opacity_off)
            self.opacity_filters[self.mainwindow.lblHasSuccess].setOpacity(1.0 if stats.last_transfer_ok else self.opacity_off)
        except KeyError:
            pass

    def generate_random_code(self, numwords=3):
        return str(secrets.randbelow(1000)) + "-" + "-".join([secrets.choice(self.code_wordlist) for _ in range(numwords)])

    @has_error_message
    def allocate_code(self,  recv_mode=False):
        textfield = self.mainwindow.txtSecretCode
        if recv_mode: textfield = self.mainwindow.txtSecretCodeRecv
        textfield.setText(self.generate_random_code(self.num_codewords))

    def got_secret_code(self, code):
        self.logger.debug("Obtained secret code: " + code)
        self.mainwindow.statusbar.showMessage(self.translator.translate("StatusMessage", "Secret code received!"), 5000)
        self.mainwindow.txtSecretCode.setText(code)
        self.update_wormhole_action_text()

    @has_error_message
    def copy_secret_code(self):
        cb = QGuiApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.mainwindow.txtSecretCode.text(), mode=cb.Clipboard)

    @has_error_message
    def paste_secret_code(self):
        text = QGuiApplication.clipboard().text()
        self.mainwindow.txtSecretCodeRecv.setText(text)

    @has_error_message
    def set_code(self, recv_mode=False):
        self.logger.debug("Requesting secret code...")
        self.mainwindow.statusbar.showMessage(self.translator.translate("StatusMessage", "Requesting secret code..."), 5000)
        try:
            text = self.mainwindow.txtSecretCode.text()
            if recv_mode: text = self.mainwindow.txtSecretCodeRecv.text()

            self.stargate.set_code(text)
            return True
        except KeyFormatError as e:
            QMessageBox.warning(self.mainwindow, "Wormhole GUI",
                                str(e),
                                QMessageBox.Ok)
            return False

    def generate_code_completion(self, partial):
        pieces = partial.split("-")
        last_piece = pieces[-1:][0]
        if last_piece == "":
            return []
        if len(pieces) <= 1:
            return []
        if last_piece in self.code_wordlist:
            return []

        candidates = list(filter(lambda i: i.startswith(last_piece),
                                 self.code_wordlist))
        trailer = "-"
        if len(pieces) >= int(self.config["app"]["num_codewords"])+1:
            trailer = ""

        return list(map(lambda c: "-".join(pieces[:-1]) + "-" + c + trailer,
                        candidates))

    def suggest_code(self, partial):
        model = self.mainwindow.txtSecretCodeRecv.completer().model()
        model.setStringList(self.generate_code_completion(partial))

    @has_error_message
    def send_text(self):
        if self.stargate.code == "":
            QMessageBox.warning(self.mainwindow, "Wormhole GUI",
                                self.translator.translate("ErrorDialog", "È necessario creare un codice segreto prima di trasmettere!"),
                                QMessageBox.Ok)
            return
        if self.mainwindow.txtMessage.toPlainText() == "":
            QMessageBox.warning(self.mainwindow, "Wormhole GUI",
                                self.translator.translate("ErrorDialog", "Il campo messaggio è vuoto!"),
                                QMessageBox.Ok)
            return
        self.stargate.send_message(self.mainwindow.txtMessage.toPlainText())
        self.mainwindow.statusbar.showMessage("Sending text...", 5000)

    @has_error_message
    def clear_received_text(self):
        self.mainwindow.txtMessageRecv.clear()

    @has_error_message
    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(self.mainwindow,
                                                  self.translator.translate("FilePicker", "Seleziona un file"),
                                                  "",
                                                  "All Files (*);")
        self.mainwindow.txtFileName.setText(filename)

    @has_error_message
    def browse_folder(self):
        foldername = QFileDialog.getExistingDirectory(self.mainwindow,
                                                      self.translator.translate("FilePicker", "Seleziona una cartella"),
                                                      "")
        self.mainwindow.txtFolderName.setText(foldername)
        self.save_settings()

    @has_error_message
    def send_file(self):
        filename = self.mainwindow.txtFileName.text()

        if self.stargate.code == "":
            QMessageBox.warning(self.mainwindow, "Wormhole GUI",
                                self.translator.translate("ErrorDialog", "È necessario creare un codice segreto prima di trasmettere!"),
                                QMessageBox.Ok)
            return
        if filename == "":
            QMessageBox.warning(self.mainwindow, "Wormhole GUI",
                                self.translator.translate("ErrorDialog", "Il campo nome-file è vuoto!"),
                                QMessageBox.Ok)
            return
        if not os.path.isfile(filename):
            QMessageBox.warning(self.mainwindow, "Wormhole GUI",
                                self.translator.translate("ErrorDialog", "Il file selezionato non esiste!"),
                                QMessageBox.Ok)
            return

        def progress_callback(partial, total, filename):
            if self.progress_counter is None:
                self.progress_counter = CustomProgressIndicator(total)
            self.progress_counter.numerator = partial
            if total != 0:
                percent = (partial * 100) / total
                self.mainwindow.progressSendFile.setValue(percent)
                if percent == 100:
                    self.mainwindow.statusbar.showMessage(self.translator.translate("StatusMessage", "Transfer complete!"), 5000)
            self.mainwindow.lblSendRate.setText(self.translator.translate("MainWindow", "Velocità: ") + str(self.progress_counter.str_rate))
            self.mainwindow.lblSendTotal.setText(self.translator.translate("MainWindow", "Inviati: ") + str(self.progress_counter.str_numerator))
            self.mainwindow.lblSendETA.setText(self.progress_counter.str_eta)


        self.stargate.progress_callback = progress_callback

        self.mainwindow.statusbar.showMessage(self.translator.translate("StatusMessage", "Sending file..."))
        self.stargate.send_file(self.mainwindow.txtFileName.text())

    def update_wormhole_action_text(self):
        if self.stargate.connected:
            self.mainwindow.actionWormhole.setText(self.translator.translate("MainWindow", "Disconnetti Wormhole"))
        else:
            self.mainwindow.actionWormhole.setText(self.translator.translate("MainWindow", "Connetti Wormhole"))

    @has_error_message
    def toggle_connect_wormhole(self):
        if self.stargate.connected:
            self.stargate.disconnect()
        else:
            self.stargate.connect()
        self.update_wormhole_action_text()

    @has_error_message
    def recv_anything(self):
        def message_callback(msg):
            if not self.mainwindow.chkAppend.isChecked():
                self.mainwindow.txtMessageRecv.clear()
            self.mainwindow.txtMessageRecv.moveCursor(QTextCursor.End)
            self.mainwindow.txtMessageRecv.insertPlainText(msg + "\n")
            self.mainwindow.txtMessageRecv.moveCursor(QTextCursor.End)
            self.mainwindow.statusbar.showMessage(self.translator.translate("StatusMessage", "Received text message"), 5000)

        def progress_callback(partial, total, filename):
            if self.progress_counter is None:
                self.progress_counter = CustomProgressIndicator(total)
            self.progress_counter.numerator = partial
            if total != 0:
                percent = (partial * 100) / total
                self.mainwindow.progressRecvFile.setValue(percent)
                if percent == 100:
                    self.mainwindow.statusbar.showMessage(self.translator.translate("StatusMessage", "Transfer complete!"), 5000)
            self.mainwindow.lblRecvRate.setText(self.translator.translate("MainWindow", "Velocità: ") + str(self.progress_counter.str_rate))
            self.mainwindow.lblRecvTotal.setText(self.translator.translate("MainWindow", "Ricevuti: ") + str(self.progress_counter.str_numerator))
            self.mainwindow.lblRecvETA.setText(self.progress_counter.str_eta)

        def offered_callback(filename, filesize):
            self.mainwindow.lblRecvFileName.setText(os.path.basename(filename))
            self.mainwindow.lcdNumber.display(filesize)
            return True

        self.stargate.message_callback = message_callback
        self.stargate.progress_callback = progress_callback
        self.stargate.offered_callback = offered_callback

        self.stargate.receive_any()
        if not self.set_code(True): return

        self.mainwindow.statusbar.showMessage(self.translator.translate("StatusMessage", "Awaiting for peer..."))

    @has_error_message
    def super_stop(self):
        self.stargate.stop_all()

