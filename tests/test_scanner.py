import pytest
from unittest.mock import patch, MagicMock
from batchalchemy.workers.scanner import FolderScanner

@pytest.fixture
def mock_scanner_deps():
    with patch("os.walk") as mock_walk:
        with patch("batchalchemy.workers.scanner.logger") as mock_logger:
            yield mock_walk, mock_logger

def test_scanner_success(mock_scanner_deps):
    mock_walk, mock_logger = mock_scanner_deps
    mock_files = [
        {"source_path": "/fake/path/file1.txt", "original_name": "file1.txt", "new_name": "file1.txt", "destination_path": "/fake/path/file1.txt", "status": "Ready"},
        {"source_path": "/fake/path/file2.txt", "original_name": "file2.txt", "new_name": "file2.txt", "destination_path": "/fake/path/file2.txt", "status": "Ready"}
    ]
    mock_walk.return_value = [("/fake/path", [], ["file1.txt", "file2.txt"])]
    
    scanner = FolderScanner("/fake/path")
    scanner.finished = MagicMock()
    scanner.progress = MagicMock()
    
    scanner.run()
    
    scanner.finished.emit.assert_called_once_with(mock_files)
    assert scanner.progress.emit.call_count == 2

def test_scanner_empty_folder(mock_scanner_deps):
    mock_walk, mock_logger = mock_scanner_deps
    mock_walk.return_value = [("/fake/empty", [], [])]
    
    scanner = FolderScanner("/fake/empty")
    scanner.finished = MagicMock()
    scanner.progress = MagicMock()
    
    scanner.run()
    
    scanner.finished.emit.assert_called_once_with([])
    assert scanner.progress.emit.call_count == 0

def test_scanner_exception(mock_scanner_deps):
    mock_walk, mock_logger = mock_scanner_deps
    mock_walk.side_effect = PermissionError("Access Denied")
    
    scanner = FolderScanner("/forbidden")
    scanner.finished = MagicMock()
    scanner.progress = MagicMock()
    
    scanner.run()
    
    scanner.finished.emit.assert_not_called()
    scanner.progress.emit.assert_not_called()
