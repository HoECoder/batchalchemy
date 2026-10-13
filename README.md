# BatchAlchemy - PySide6 Edition

BatchAlchemy is a high-precision desktop application for complex bulk file renaming and moving operations. It features a spreadsheet-style grid for manual cell-level overrides combined with a powerful Rule Engine for automated batch processing.

## Architecture & Design

For a detailed breakdown of the system architecture, component relationships, and data flow, please refer to the [Architecture Documentation](ARCHITECTURE.md).

## AI/LLM Disclaimer

I developed this with help from an LLM running on my local machine. Models were strictly local on my own GPU. I utilized gemm4 with a 12B and 26B parameter model, using opencode.

I've conducted the reviews.

## Features

- **Smart Rule Engine**: Define global rules using:
  - **Search & Replace**: Global string substitution.
  - **Regex Support**: Complex pattern matching and replacement.
  - **Prefix/Suffix**: Add strings to the start or end of filenames.
- **Spreadsheet Grid**:
  - Editable "New Name" and "Destination Path" fields.
  - Real-time collision detection (flags files in red if the target exists).
  - Proactive permission checks (flags files in yellow if the destination is unwritable).
- **Execution & Safety**:
  - **Dry Run Mode**: Preview exact changes, collision counts, and permission errors before committing.
  - **Multi-core Processing**: Uses `QThreadPool` and `QRunnable` for non-blocking, parallel file I/O.
  - **Undo Buffer**: Revert up to 50 manual edits with a single click.
- **Logging & UX**:
    - Dual-output logging (File + UI Console).
    - Dark and Light theme support.
    - Real-time Search/Filter bar.

## Technical Stack

- **Language**: Python 3.14+
- **GUI Framework**: PySide6 (Qt for Python)
- **Environment**: `uv` (package management and virtual environments)
- **Concurrency**: `QThreadPool`, `QRunnable`
- **Testing**: `pytest`, `pytest-mock`

## Getting Started

### Prerequisites
Ensure you have `uv` installed.

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd batchalchemy
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Running the App
```bash
uv run batchalchemy
```

### Running Tests
```bash
export PYTHONPATH=$PYTHONPATH:.
uv run pytest tests/
```

## Development Roadmap
- [x] Phase 1: PySide6 Boilerplate & Folder Scanner
- [x] Phase 2: Editable Grid & Model Implementation
- [x] Phase 3: Rule Engine (Regex, Prefix, Suffix)
- [x] Phase 4: Multi-core Threading & Logging System
- [x] Phase 5: Collision Detection & Dry Run logic
- [x] Phase 6: UX Polishing (Themes, Search, Undo)
- [x] Quality Assurance: Unit Tests & Coverage

