from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
import os
from copy import deepcopy

class FileTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._original_data = data or []
        self._data = []
        self.history = []
        self.refresh_data()

    def refresh_data(self, query: str = ""):
        # Sort the original data by source_path first
        sorted_data = sorted(self._original_data, key=lambda x: x["source_path"])
        
        self._data = []
        for item in sorted_data:
            if not query or (query.lower() in item["original_name"].lower() or 
                             query.lower() in item["source_path"].lower() or 
                             query.lower() in item["new_name"].lower()):
                self._data.append(item.copy())
        self.refresh_statuses()
        self.layoutChanged.emit()
        self.layoutChanged.emit()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 6  # Index, Source Path, Original Name, New Name, Destination Path, Status

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ["Index", "Source Path", "Original Name", "New Name", "Destination Path", "Status"]
                return headers[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row_data = self._data[index.row()]
            if index.column() == 0:
                return index.row() + 1
            elif index.column() == 1:
                return row_data["source_path"]
            elif index.column() == 2:
                return row_data["original_name"]
            elif index.column() == 3:
                return row_data["new_name"]
            elif index.column() == 4:
                return row_data["destination_path"]
            elif index.column() == 5:
                return row_data["status"]
        elif role == Qt.BackgroundRole:
            row_data = self._data[index.row()]
            if index.column() == 5:
                if "Collision" in row_data["status"]:
                    return Qt.GlobalColor.red
                elif "Permission" in row_data["status"]:
                    return Qt.GlobalColor.yellow
                elif "Ready" in row_data["status"]:
                    return Qt.GlobalColor.green
        return None

    def flags(self, index):
        if index.column() in [3, 4]:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsEnabled

    def set_data(self, data):
        self._original_data = data
        self.refresh_data()

    def refresh_statuses(self, row_index: int = None):
        """Updates the status of all items based on collision and permissions.
        If row_index is provided, only updates that specific row.
        """
        if row_index is not None:
            row_data = self._data[row_index]
            source = row_data.get("source_path")
            dest = row_data.get("destination_path")
            if not source or not dest:
                return

            # Proactive Permission Check
            dest_dir = os.path.dirname(dest)
            if not os.access(dest_dir, os.W_OK):
                row_data["status"] = "Permission Error"
                return

            # Collision Detection
            if os.path.exists(dest) and dest != source:
                row_data["status"] = "Collision"
            else:
                row_data["status"] = "Ready"
        else:
            for row_data in self._data:
                source = row_data.get("source_path")
                dest = row_data.get("destination_path")
                if not source or not dest:
                    continue
                
                # Proactive Permission Check
                dest_dir = os.path.dirname(dest)
                if not os.access(dest_dir, os.W_OK):
                    row_data["status"] = "Permission Error"
                    continue
                
                # Collision Detection
                if os.path.exists(dest) and dest != source:
                    row_data["status"] = "Collision"
                else:
                    row_data["status"] = "Ready"

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            col = index.column()
            
            if col not in [3, 4]:
                return False
            
            if value is None:
                return False

            # Save to history before change
            self.history.append(deepcopy(self._data))
            if len(self.history) > 50:
                self.history.pop(0)
            
            # Update the specific field
            if col == 3:  # New Name
                self._data[row]["new_name"] = str(value)
                self._data[row]["manually_edited"] = True
            elif col == 4:  # Destination Path
                self._data[row]["destination_path"] = str(value)
                self._data[row]["manually_edited"] = True
            
            # Update the status for only this row silently
            self.refresh_statuses(row)
            
            # Notify the view that the specific columns being edited have changed.
            # This prevents the view from getting confused by updates to other columns (like status).
            self.dataChanged.emit(self.index(row, col), self.index(row, col))
            return True
        return False




    def undo(self):
        if self.history:
            self._data = self.history.pop()
            self.refresh_statuses()
            self.dataChanged.emit(self.index(0, 0), self.index(len(self._data)-1, 5))
            return True
        return False
