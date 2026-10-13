import pytest
from unittest.mock import patch
from batchalchemy.models.file_model import FileTableModel

@pytest.fixture
def sample_data():
    return [
        {
            "source_path": "/path/to/file1.txt",
            "original_name": "file1.txt",
            "new_name": "file1.txt",
            "destination_path": "/path/to/file1.txt",
            "status": "Ready",
            "manually_edited": False
        },
        {
            "source_path": "/path/to/file2.txt",
            "original_name": "file2.txt",
            "new_name": "file2.txt",
            "destination_path": "/path/to/collision.txt",
            "status": "Ready",
            "manually_edited": False
        }
    ]

def test_refresh_statuses_collision(sample_data):
    model = FileTableModel(sample_data)
    
    with patch("os.path.exists") as mock_exists:
        # file1.txt exists (same as source, should be ready)
        # collision.txt exists (different from source, should be collision)
        mock_exists.side_effect = lambda p: p == "/path/to/collision.txt"
        
        with patch("os.access", return_value=True):
            model.refresh_statuses()
            
            assert model._data[1]["status"] == "Collision"
            assert model._data[0]["status"] == "Ready"

def test_refresh_statuses_permission_error(sample_data):
    model = FileTableModel(sample_data)
    
    with patch("os.path.exists", return_value=False):
        # Mock os.access to return False for the directory path
        with patch("os.access", return_value=False):
            model.refresh_statuses()
            
            assert model._data[0]["status"] == "Permission Error"

def test_set_data_updates_status(sample_data):
    model = FileTableModel(sample_data)
    
    with patch("os.path.exists", return_value=True):
        with patch("os.access", return_value=True):
            # Manually edit file1's destination to a collision path
            model.setData(model.index(0, 4), "/path/to/collision.txt")
            assert model._data[0]["destination_path"] == "/path/to/collision.txt"
            assert model._data[0]["manually_edited"] is True
            assert model._data[0]["status"] == "Collision"

def test_undo_functionality(sample_data):
    model = FileTableModel(sample_data)
    
    # Change file1 name
    model.setData(model.index(0, 3), "changed_name.txt")
    assert model._data[0]["new_name"] == "changed_name.txt"
    
    # Undo
    assert model.undo() is True
    assert model._data[0]["new_name"] == "file1.txt"
    
    # Undo again (should be False as history empty)
    assert model.undo() is False

def test_refresh_data_filtering(sample_data):
    model = FileTableModel(sample_data)
    
    # Filter by name
    model.refresh_data("file1")
    assert len(model._data) == 1
    assert model._data[0]["original_name"] == "file1.txt"
    
    # Filter by path
    model.refresh_data("/path/to/file2")
    assert len(model._data) == 1
    assert model._data[0]["source_path"] == "/path/to/file2.txt"

def test_undo_history_limit(sample_data):
    model = FileTableModel(sample_data)
    
    # Perform 60 edits to exceed the 50 limit
    for i in range(60):
        model.setData(model.index(0, 3), f"name_{i}.txt")
    
    # History should have 50 items
    assert len(model.history) == 50
    
    # Undo should work
    assert model.undo() is True
    assert "name_59" not in model._data[0]["new_name"]

def test_refresh_statuses_mixed(sample_data):
    model = FileTableModel(sample_data)
    
    def mock_exists(p):
        return p == "/path/to/collision.txt" or p == "/path/to/file1.txt"
    
    def mock_access(p, mode):
        # Let's make /path/to unwritable
        return p != "/path/to"
        
    with patch("os.path.exists", side_effect=mock_exists):
        with patch("os.access", side_effect=mock_access):
            model.refresh_statuses()
            
            # If /path/to is unwritable, it should be Permission Error for both
            assert model._data[0]["status"] == "Permission Error"
            assert model._data[1]["status"] == "Permission Error"

def test_refresh_data_empty_query(sample_data):
    model = FileTableModel(sample_data)
    model.refresh_data("")
    assert len(model._data) == 2

def test_set_data_non_editable_column(sample_data):
    model = FileTableModel(sample_data)
    # Column 0 is Index, not editable
    success = model.setData(model.index(0, 0), "New Index")
    assert success is False

def test_refresh_data_no_match(sample_data):
    model = FileTableModel(sample_data)
    model.refresh_data("nonexistent_file_xyz")
    assert len(model._data) == 0

def test_undo_nothing_to_undo(sample_data):
    model = FileTableModel(sample_data)
    assert model.undo() is False

def test_refresh_statuses_no_files(sample_data):
    model = FileTableModel([])
    model.refresh_statuses()
    assert len(model._data) == 0
