from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Signal, QObject

class LogConsole(QWidget):
    log_message = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)
        
        self.log_message.connect(self.append_message)

    def append_message(self, message):
        self.text_edit.append(message)
