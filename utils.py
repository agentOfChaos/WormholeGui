import traceback
from PySide2.QtWidgets import QMessageBox


def has_error_message(old_function):
    def wrapper(*args, **kwds):
        try:
            return old_function(*args, **kwds)
        except Exception:
            error = traceback.format_exc()
            app = args[0]
            QMessageBox.critical(app.mainwindow, "Wormhole GUI",
                                 error,
                                 QMessageBox.Ok)
            return None

    return wrapper
