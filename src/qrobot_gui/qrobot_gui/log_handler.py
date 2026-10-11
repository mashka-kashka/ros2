import logging

from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import pyqtSignal, QObject

class QLogHandler(QObject, logging.Handler):
    appendText = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.appendText.connect(self._append_text)

    def emit(self, record):
        log_message = self.format(record)
        self.appendText.emit(log_message)

    def _append_text(self, text):
        if self.parent:
            self.parent.append(text)