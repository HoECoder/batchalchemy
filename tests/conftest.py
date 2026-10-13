import pytest
from PySide6.QtWidgets import QApplication
import sys

_app = None

@pytest.fixture(scope="session")
def qapp():
    global _app
    if _app is None:
        _app = QApplication(sys.argv)
    yield _app
    # Note: We don't destroy it here to avoid issues with other tests 
    # that might still need it, but in a perfect world we would.
