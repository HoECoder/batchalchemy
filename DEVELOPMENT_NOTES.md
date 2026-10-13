# Development Notes & Debugging Tricks

This document captures specific patterns, fixes, and "tricks" discovered while developing and debugging the BatchAlchemy project.

## PySide6 & UI Testing

### QApplication Singleton
- **Problem**: Trying to instantiate `QApplication` multiple times in tests causes `RuntimeError: libshiboken: Please destroy the QApplication singleton before creating a new QApplication instance.`
- **Fix**: Use a session-scoped fixture in `conftest.py` to create a single `QApplication` instance for all tests.

### Mocking Widgets & Signals
- **Mocking Signals**: To verify signals are emitted (e.g., `log_message`), mock the signal object itself and its `emit` method.
    - *Trick*: `window.log_console.log_message = MagicMock()`, then verify with `window.log_console.log_message.emit.assert_called_once()`.
- **Mocking UI Elements**: When testing `MainWindow` logic, mock `summary_label`, `log_console`, and `setStyleSheet` to avoid interacting with the actual rendering engine.

### Mocking Class Instantiation
- **Problem**: Methods like `add_folder` create new instances of classes (e.g., `FolderScanner`). Simple attribute mocking doesn't work because the instance is created *inside* the method.
- **Fix**: Patch the class itself in the target module.
    - *Example*: `with patch("batchalchemy.views.main_window.FolderScanner") as MockScanner:`
    - *Trick*: Assign the `return_value` of the mock to a local variable to track calls on the resulting instance.

## Filesystem & Concurrency

### QFileDialog Cancellation
- **Problem**: `folder_path, _ = QFileDialog.getExistingDirectory(...)` raises `ValueError: not enough values to unpack` if the user clicks "Cancel".
- **Fix**: Assign the return value to a single variable: `folder_path = QFileDialog.getExistingDirectory(...)`.

### ProcessPoolExecutor & Signals
- **Pattern**: Use `ProcessPoolExecutor` for heavy file operations (renaming) to keep the UI responsive.
- **Pattern**: Wrap the executor in a `QObject` (like `RenameTask`) to bridge the gap between the thread pool and PySide6's signal system.

### Namespace Management
- **Rule**: All internal imports must use the package-level `batchalchemy` namespace (e.g., `from batchalchemy.utils.logger import logger`).
- **Fix**: Ensure `__init__.py` is handled correctly and `pyproject.toml` points to the correct entry point to support `uvx` / `pipx` installations.

## Testing & Coverage

### Mocking `os` for Tests
- **Pattern**: Use `patch("os.path.exists")` and `patch("os.access")` extensively in `FileTableModel` tests to simulate collisions and permission errors without touching the real filesystem.

### Coverage Gaps
- **Observation**: High-level UI classes (`MainWindow`) naturally have lower coverage because most logic is delegated to models and workers.
- **Strategy**: Focus on unit testing the logic in `RuleEngine`, `FileTableModel`, and `FolderScanner`, as these are the core "engines" of the application.
