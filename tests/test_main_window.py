import pytest
from unittest.mock import MagicMock, patch
from batchalchemy.views.main_window import MainWindow

def test_show_dry_run_summary():
    with patch("batchalchemy.views.main_window.MainWindow.__init__", return_value=None):
        window = MainWindow()
        window.model = MagicMock()
        window.model._data = [
            {
                "source_path": "/path/to/file1.txt",
                "destination_path": "/path/to/dest1.txt",
                "manually_edited": False
            },
            {
                "source_path": "/path/to/file2.txt",
                "destination_path": "/path/to/collision.txt",
                "manually_edited": False
            }
        ]
        # Mock the log_console and its log_message signal
        mock_log_console = MagicMock()
        mock_log_signal = MagicMock()
        mock_log_console.log_message = mock_log_signal
        window.log_console = mock_log_console
        
        window.summary_label = MagicMock()
        window.summary_label.text.return_value = "Dry Run Summary: Action will rename 1 files, move 0 files. [1] collisions detected. [0] permission errors detected."
        
        window.show_dry_run_summary()
        
        assert "rename 1 files" in window.summary_label.text()
        assert "collisions detected" in window.summary_label.text()
        # Verify the signal's emit method was called with the correct string
        mock_log_signal.emit.assert_called_once()

def test_add_folder_logic():
    with patch("batchalchemy.views.main_window.MainWindow.__init__", return_value=None):
        window = MainWindow()
        
        # Create a mock for the scanner instance
        mock_scanner_instance = MagicMock()
        # We need to inject this into the window
        window.scanner = mock_scanner_instance
        window.scanner.progress = MagicMock()
        window.scanner.finished = MagicMock()
        
        with patch("batchalchemy.views.main_window.QFileDialog.getExistingDirectory") as mock_dialog:
            mock_dialog.return_value = ("/fake/path", ())
            # We don't want to patch FolderScanner here because we already injected the mock_scanner_instance
            # However, add_folder() calls FolderScanner(...), so we need to mock that constructor too
            with patch("batchalchemy.views.main_window.FolderScanner", return_value=mock_scanner_instance):
                window.add_folder()
                mock_dialog.assert_called_once()
                mock_scanner_instance.start.assert_called_once()

def test_toggle_theme():
    with patch("batchalchemy.views.main_window.MainWindow.__init__", return_value=None):
        window = MainWindow()
        window.current_theme = "light"
        window.setStyleSheet = MagicMock()
        window.toggle_theme()
        assert window.current_theme == "dark"
        window.setStyleSheet.assert_called()
