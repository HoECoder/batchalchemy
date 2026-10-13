import pytest
from unittest.mock import patch
from batchalchemy.workers.rename_task import RenameTask

def test_rename_task_dry_run():
    task = RenameTask("/src/file.txt", "/dest/file.txt", dry_run=True)
    result = task.execute_rename()
    assert "Dry Run" in result
    assert "/src/file.txt" in result
    assert "/dest/file.txt" in result

def test_rename_task_collision():
    with patch("os.path.exists") as mock_exists:
        # First call: /dest/file.txt exists (True)
        # Second call: /dest/file_1.txt exists (False)
        mock_exists.side_effect = [True, False]
        
        with patch("os.access", return_value=True):
            with patch("os.rename"):
                task = RenameTask("/src/file.txt", "/dest/file.txt", dry_run=False)
                result = task.execute_rename()
                
                assert "Success" in result
                assert "_1.txt" in result

def test_rename_task_permission_denied():
    with patch("os.path.exists", return_value=False):
        with patch("os.access", return_value=False):
            task = RenameTask("/src/file.txt", "/dest/file.txt", dry_run=False)
            result = task.execute_rename()
            
            assert "Error: Permission Denied" in result

def test_rename_task_general_exception():
    with patch("os.path.exists", return_value=False):
        with patch("os.access", return_value=True):
            with patch("os.rename", side_effect=OSError("Disk Full")):
                task = RenameTask("/src/file.txt", "/dest/file.txt", dry_run=False)
                result = task.execute_rename()
                assert "Error: /src/file.txt -> Disk Full" in result
