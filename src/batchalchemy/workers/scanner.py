import os
from PySide6.QtCore import QThread, Signal
from batchalchemy.utils.logger import logger

class FolderScanner(QThread):
    finished = Signal(list)
    progress = Signal(int)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        logger.info(f"Starting scan in folder: {self.folder_path}")
        files = []
        try:
            for root, dirs, filenames in os.walk(self.folder_path):
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    files.append({
                        "source_path": full_path,
                        "original_name": filename,
                        "new_name": filename,
                        "destination_path": full_path,
                        "status": "Ready"
                    })
                    self.progress.emit(len(files))
            logger.info(f"Scan completed. Found {len(files)} files.")
            self.finished.emit(files)
        except Exception as e:
            logger.error(f"Error scanning folder: {e}")
