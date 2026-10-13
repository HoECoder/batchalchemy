# Project Roadmap

## 🚀 Planned Features

### 1. Advanced Auto-Numbering
- **Description:** Allow users to apply sequential numbering to selected files and use an `{autonum}` sentinel in renaming rules.
- **Key Capabilities:** Custom start values, step increments, and padding support (e.g., `001`).

### 2. Detailed Logging & Shell Export
- **Description:** Enhance logging and provide command execution exports.
- **Logging:** Dual-destination (UI and file) with log rotation and high-granularity messaging (Dry Run, Execute, Success, Error).
- **Export:** Cross-platform shell script generation (`.sh` for Unix, `.bat` for Windows) with automatic directory creation and path escaping.

### 3. Native Language Support (i18n/L10n)
- **Description:** Implement full internationalization using Qt's translation system.
- **Key Capabilities:** Dynamic runtime language switching and external `.qm` translation files.

### 4. Log Console Syntax Highlighting
- **Description:** Improve log readability in the UI.
- **Key Capabilities:** Color-coded messages based on severity (Error, Warning, Success, etc.) using `QSyntaxHighlighter`.

## 🛠️ Enhancements & Fixes

### File Model Optimizations
- **Redundant Signal Fix:** Remove duplicate layout change signals to prevent unnecessary UI redraws.
- **Status Refresh Optimization:** Offload filesystem I/O to background threads and implement throttling for status checks.
- **Undo Mechanism Refinement:** Implement an incremental command pattern for undo/redo to support large datasets without performance degradation.

### Rename Task Refinements
- **Collision Detection:** Improve renaming intelligence to handle complex scenarios, such as existing numbering patterns and multi-part extensions (e.g., `.tar.gz`).
