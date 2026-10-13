# Internal API Reference

This document provides a technical reference for the internal classes, methods, and functions within the BatchAlchemy project.

## Core Models

### `batchalchemy.models.file_model.FileTableModel`
*Subclass of `QAbstractTableModel`*

Manages the state and data for the file list displayed in the `QTableView`.

- **`__init__(self, data=None)`**: Initializes the model. Maintains `_original_data` (source of truth), `_data` (currently filtered/displayed), and a `history` buffer for undoing edits.
- **`refresh_data(self, query: str = "")`**: Sorts `_original_data` by `source_path`, filters the list based on the `query` (matching `original_name`, `source_path`, or `new_name`), and emits `layoutChanged`.
- **`rowCount(self, parent=QModelIndex()) -> int`**: Returns the number of rows in the current filtered view.
- **`columnCount(self, parent=QModelIndex()) -> int`**: Returns 6.
- **`headerData(self, section, orientation, role)`**: Returns the following column headers: `["Index", "Source Path", "Original Name", "New Name", "Destination Path", "Status"]`.
- **`data(self, index, role=Qt.DisplayRole)`**:
    - `Qt.DisplayRole` / `Qt.EditRole`: Returns cell value.
    - `Qt.BackgroundRole`: Returns `Qt.GlobalColor.red` for "Collision" status, `Qt.GlobalColor.yellow` for "Permission Error", and `Qt.GlobalColor.green` for "Ready" status.
- **`flags(self, index)`**: Returns `Qt.ItemIsEnabled | Qt.ItemIsEditable` for the "New Name" and "Destination Path" columns.
- **`set_data(self, data)`**: Replaces the entire dataset and triggers a refresh.
- **`refresh_statuses(self, row_index: int = None)`**: Performs proactive checks for each file:
    - **Permissions**: Checks if the destination directory is writable using `os.access(dest_dir, os.W_OK)`.
    - **Collisions**: Checks if `os.path.exists(dest)` is true (and `dest != source`).
- **`setData(self, index, value, role=Qt.EditRole)`**: Updates a specific cell, marks the row as `manually_edited = True`, saves the previous state to `history` (up to 50 steps), and emits `dataChanged`.
- **`undo(self) -> bool`**: Restores the state from the last entry in `history`.

## Workers & Logic Engines

### `batchalchemy.workers.scanner.FolderScanner`
*Subclass of `QThread`*

Performs non-blocking filesystem traversal.

- **Signals**:
    - `finished(list)`: Emitted when traversal is complete, containing a list of file dictionaries.
    - `progress(int)`: Emitted every time a new file is discovered.
- **`__init__(self, folder_path)`**: Initializes with a target directory.
- **`run(self)`**: Executes `os.walk` to build the file list.

### `batchalchemy.workers.rule_engine.RuleEngine`
*Class*

A stateless engine that applies transformations sequentially to filenames.

- **`add_search_replace(self, search: str, replace: str)`**: Adds a literal string substitution rule.
- **`add_regex(self, pattern: str, replace: str)`**: Adds a regex-based substitution rule.
- **`add_prefix(self, prefix: str)`**: Adds a rule to prepend text to the filename.
- **`add_suffix(self, suffix: str)`**: Adds a rule to append text before the file extension.
- **`apply_rules(self, filenames: List[str]) -> List[str]`**: Returns a new list of filenames with all active rules applied.

### `batchalchemy.workers.rename_task.RenameTask`
*Subclass of `QObject`*

Orchestrates parallel renaming operations.

- **`__init__(self, source_path=None, dest_path=None, dry_run=False)`**: Initializes the task.
- **`run_batch(self, tasks: List[Tuple[str, str]], callback: Callable, dry_run: bool = False)`**: Uses a `ProcessPoolExecutor` to execute `rename_file` for all tasks in the list.
- **`execute_rename(self)`**: Executes a single rename operation for the task's own `source_path` and `dest_path`.

### `batchalchemy.workers.rename_task.rename_file`
*Standalone Function*

The atomic operation performed by worker processes.

- **Parameters**: `source_path (str)`, `dest_path (str)`, `dry_run (bool)`.
- **Behavior**: 
    - If `dry_run` is True, logs the action and returns.
    - Performs collision detection by incrementing filename with `_1`, `_2`, etc.
    - Performs permission checks on the destination directory.
    - Executes `os.rename`.

## Views & Widgets

### `batchalchemy.views.main_window.MainWindow`
*Subclass of `QMainWindow`*

The application's main controller.

- **`apply_theme(self, theme: str)`**: Applies Light or Dark QSS stylesheets.
- **`toggle_theme(self)`**: Toggles the current theme.
- **`add_folder(self)`**: Starts the `FolderScanner` for a user-selected directory.
- **`on_scan_finished(self, files)`**: Populates the `FileTableModel` with the discovered files.
- **`filter_data(self, text: str)`**: Updates the model's visible data based on a search string.
- **`apply_rules_logic(self, engine: RuleEngine)`**: Applies the rules from the `RuleEngine` to the model's "New Name" column for all non-manually-edited files.
- **`undo_action(self)`**: Triggers the model's undo mechanism.
- **`commit_batch(self)`**: Spawns a background `threading.Thread` to run `RenameTask.run_batch` to avoid blocking the UI.
- **`show_dry_run_summary(self)`**: Calculates and displays statistics (rename vs. move, collision count, permission errors).
- **`on_rename_result(self, result: str)`**: Updates the model's "Status" column to "Done" if the result indicates success.

### `batchalchemy.views.widgets.rule_panel.RulePanel`
*Subclass of `QWidget`*

Input widget for rule configuration.

- **`get_rules(self) -> RuleEngine`**: Collects all active inputs (Search/Replace, Regex, Prefix, Suffix) and returns a configured `RuleEngine`.
- **`handle_apply(self)`**: Calls the provided callback with the generated `RuleEngine`.

### `batchalchemy.views.widgets.log_console.LogConsole`
*Subclass of `QWidget`*

A thread-safe display for application logs.

- **Signals**:
    - `log_message(str)`: Emitted when a new log line is sent to the console.
- **`append_message(self, message: str)`**: Appends a message to the internal `QTextEdit`.

## Utilities

### `batchalchemy.utils.logger.logger`
*Module-level singleton*

Configured to output to:
- `rename_history.log` (File handler, `INFO` level)
- `sys.stdout` (Stream handler, `INFO` level)
