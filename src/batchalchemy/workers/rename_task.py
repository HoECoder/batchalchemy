import os
from concurrent.futures import ProcessPoolExecutor
from PySide6.QtCore import QObject, Signal
from batchalchemy.utils.logger import logger

class RenamerSignals(QObject):
    result_received = Signal(str)

class RenameTask(QObject):
    def __init__(self, source_path=None, dest_path=None, dry_run=False):
        super().__init__()
        self.source_path = source_path
        self.dest_path = dest_path
        self.dry_run = dry_run
        self.executor = ProcessPoolExecutor()
        self.signals = RenamerSignals()

    def run_batch(self, tasks, callback, dry_run=False):
        def handle_result(result):
            callback(result)

        futures = []
        for source, dest in tasks:
            futures.append(self.executor.submit(rename_file, source, dest, dry_run))
        
        for future in futures:
            try:
                result = future.result()
                handle_result(result)
            except Exception as e:
                logger.error(f"Batch execution error: {e}")
                handle_result(f"Error: {e}")

    def execute_rename(self):
        result = rename_file(self.source_path, self.dest_path, self.dry_run)
        return result

def rename_file(source_path, dest_path, dry_run=False):
    if dry_run:
        logger.info(f"Dry Run: {source_path} -> {dest_path}")
        return f"Dry Run: {source_path} -> {dest_path}"

    base, ext = os.path.splitext(dest_path)
    counter = 1
    final_dest = dest_path

    # Collision Detection & Incrementing
    while os.path.exists(final_dest) and final_dest != source_path:
        final_dest = f"{base}_{counter}{ext}"
        counter += 1

    try:
        # Permission Check: Check if destination directory is writable
        dest_dir = os.path.dirname(final_dest)
        if not os.access(dest_dir, os.W_OK):
            logger.error(f"Permission Denied (Write) on {dest_dir}")
            return f"Error: Permission Denied (Write) on {dest_dir}"

        os.rename(source_path, final_dest)
        logger.info(f"Success: {source_path} -> {final_dest}")
        return f"Success: {source_path} -> {final_dest}"
    except Exception as e:
        logger.error(f"Error: {source_path} -> {e}")
        return f"Error: {source_path} -> {e}"
