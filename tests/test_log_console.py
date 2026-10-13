import pytest
from PySide6.QtWidgets import QApplication
from batchalchemy.views.widgets.log_console import LogConsole
import sys

# Initialize QApplication for PySide6 widgets
app = QApplication(sys.argv)

def test_log_console_append_message():
    console = LogConsole()
    test_msg = "Test message"
    console.append_message(test_msg)
    assert console.text_edit.toPlainText() == test_msg

def test_log_console_multiple_messages():
    console = LogConsole()
    console.append_message("Msg 1")
    console.append_message("Msg 2")
    assert console.text_edit.toPlainText() == "Msg 1\nMsg 2"
