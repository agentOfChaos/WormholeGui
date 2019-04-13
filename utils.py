import traceback
import os, sys, subprocess
from PySide2.QtWidgets import QMessageBox, QGraphicsOpacityEffect
from transitions import MachineError


def has_error_message(old_function):
    def wrapper(*args, **kwds):
        try:
            return old_function(*args, **kwds)
        except MachineError:
            error = traceback.format_exc()
            app = args[0]
            app.orchestrator.error(desc=error)
        except Exception:
            error = traceback.format_exc()
            app = args[0]
            app.logger.critical(error)
            if hasattr(app, "mainwindow:"):
                QMessageBox.critical(app.mainwindow, "Wormhole GUI",
                                     error,
                                     QMessageBox.Ok)
            return None

    return wrapper


def has_orchestrator_error_message(old_function):
    def wrapper(*args, **kwds):
        try:
            return old_function(*args, **kwds)
        except MachineError:
            error = traceback.format_exc()
            app = args[0]
            app.orchestrator.error(desc=error)
    return wrapper


def init_label_opacity(app, label, initial_opacity=1.0):
    app.opacity_filters[label] = QGraphicsOpacityEffect()
    label.setGraphicsEffect(app.opacity_filters[label])
    app.opacity_filters[label].setOpacity(initial_opacity)


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
