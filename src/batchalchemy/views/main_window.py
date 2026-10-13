import sys
import os
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QTableView, QPushButton, QFileDialog, QHBoxLayout, QLineEdit, QCheckBox
from PySide6.QtCore import Qt
from batchalchemy.models.file_model import FileTableModel
from batchalchemy.workers.scanner import FolderScanner
from batchalchemy.views.widgets.rule_panel import RulePanel
from batchalchemy.views.widgets.log_console import LogConsole
from batchalchemy.workers.rename_task import RenameTask
from PySide6.QtCore import QThreadPool
from batchalchemy.utils.logger import logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BatchAlchemy")
        self.resize(1200, 800)
        self.current_theme = "light"

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel("BatchAlchemy - File Renamer")
        layout.addWidget(self.label)

        toolbar_layout = QHBoxLayout()
        self.btn_add_folder = QPushButton("Add Folder")
        self.btn_add_folder.clicked.connect(self.add_folder)
        toolbar_layout.addWidget(self.btn_add_folder)
        
        self.btn_commit = QPushButton("Commit")
        self.btn_commit.setEnabled(False)
        self.btn_commit.clicked.connect(self.commit_batch)
        toolbar_layout.addWidget(self.btn_commit)

        self.dry_run_checkbox = QCheckBox("Dry Run")
        toolbar_layout.addWidget(self.dry_run_checkbox)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Filter by name, path, or status...")
        self.search_bar.textChanged.connect(self.filter_data)
        toolbar_layout.addWidget(self.search_bar)

        self.btn_undo = QPushButton("Undo")
        self.btn_undo.setEnabled(False)
        self.btn_undo.clicked.connect(self.undo_action)
        toolbar_layout.addWidget(self.btn_undo)
        
        self.theme_toggle = QPushButton("Toggle Theme")
        self.theme_toggle.clicked.connect(self.toggle_theme)
        toolbar_layout.addWidget(self.theme_toggle)
        
        layout.addLayout(toolbar_layout)

        self.rule_panel = RulePanel(self.apply_rules_logic)
        layout.addWidget(self.rule_panel)

        self.table_view = QTableView()
        self.model = FileTableModel()
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)

        self.summary_label = QLabel("")
        self.summary_label.setStyleSheet("font-weight: bold; color: #333; margin-top: 10px;")
        layout.addWidget(self.summary_label)

        self.log_console = LogConsole()
        layout.addWidget(self.log_console)

        self.statusBar().showMessage("Ready")
        self.apply_theme("light")

        self.thread_pool = QThreadPool()

    def apply_theme(self, theme):
        self.current_theme = theme
        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QTableView {
                    gridline-color: #444;
                    
                    color: #ffffff;
                }
                QHeaderView::section {
                    background-color: #444;
                    padding: 4px;
                    border: 1px solid #555;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #444;
                    color: #ffffff;
                    border: 1px solid #666;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
                QLineEdit {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #555;
                    padding: 3px;
                }
                QCheckBox {
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QTableView {
                    gridline-color: #d3d3d3;
                    
                    color: #000000;
                }
                QHeaderView::section {
                    background-color: #eee;
                    padding: 4px;
                    border: 1px solid #ccc;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: #000000;
                    border: 1px solid #ccc;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #ccc;
                    padding: 3px;
                }
                QCheckBox {
                    color: #000000;
                }
                QLabel {
                    color: #000000;
                }
            """)

    def toggle_theme(self):
        if self.current_theme == "light":
            self.apply_theme("dark")
        else:
            self.apply_theme("light")

    def add_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.scanner = FolderScanner(folder_path)
            self.scanner.progress.connect(self.update_progress)
            self.scanner.finished.connect(self.on_scan_finished)
            self.scanner.start()

    def update_progress(self, count):
        self.statusBar().showMessage(f"Scanning... {count} files found.")

    def on_scan_finished(self, files):
        self.model.set_data(files)
        self.btn_commit.setEnabled(True)
        self.statusBar().showMessage("Scan complete.", 5000)
        self.table_view.resizeColumnsToContents()

    def filter_data(self, text):
        self.model.refresh_data(text)

    def apply_rules_logic(self, engine):
        for row in range(self.model.rowCount()):
            row_data = self.model._data[row]
            if not row_data.get("manually_edited", False):
                original_name = row_data["original_name"]
                new_name = engine.apply_rules([original_name])[0]
                
                idx = self.model.index(row, 3) # New Name column
                self.model.setData(idx, new_name)
        
        self.btn_undo.setEnabled(len(self.model._data) > 0)

    def undo_action(self):
        if self.model.undo():
            self.btn_undo.setEnabled(len(self.model._data) > 0)
            self.statusBar().showMessage("Undo successful", 3000)

    def commit_batch(self):
        if self.dry_run_checkbox.isChecked():
            self.show_dry_run_summary()
            return

        tasks = []
        for row in range(self.model.rowCount()):
            row_data = self.model._data[row]
            tasks.append((row_data["source_path"], row_data["destination_path"]))
        
        self.btn_commit.setEnabled(False)
        self.btn_add_folder.setEnabled(False)
        
        self.renamer = RenameTask()
        self.renamer.signals.result_received.connect(self.on_rename_result)
        
        def run():
            self.renamer.run_batch(tasks, self.renamer.signals.result_received.emit, 
                                    dry_run=False)
        
        import threading
        threading.Thread(target=run, daemon=True).start()

    def show_dry_run_summary(self):
        rename_count = 0
        move_count = 0
        collision_count = 0
        permission_error_count = 0

        for row_data in self.model._data:
            source = row_data["source_path"]
            dest = row_data["destination_path"]
            
            # Check for move vs rename
            if os.path.dirname(source) != os.path.dirname(dest):
                move_count += 1
            else:
                rename_count += 1
            
            # Check for collision
            if os.path.exists(dest) and dest != source:
                collision_count += 1
            
            # Check for permission error
            dest_dir = os.path.dirname(dest)
            if not os.access(dest_dir, os.W_OK):
                permission_error_count += 1

        summary = (f"Dry Run Summary: "
                   f"Action will rename {rename_count} files, move {move_count} files. "
                   f"[{collision_count}] collisions detected. "
                   f"[{permission_error_count}] permission errors detected.")
        self.summary_label.setText(summary)
        self.log_console.log_message.emit(summary)

    def on_rename_result(self, result):
        self.log_console.log_message.emit(result)
        if "Success" in result and "Dry Run" not in result:
            for i, row_data in enumerate(self.model._data):
                if row_data["source_path"] in result:
                    idx = self.model.index(i, 5) # Status column
                    self.model.setData(idx, "Done")
                    break
