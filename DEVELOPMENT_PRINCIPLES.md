# Development Principles & Engineering Standards

This document outlines the core architectural and engineering principles to be followed for all projects developed with this assistant. These principles ensure high-quality, testable, and maintainable software.

## 1. Architectural Patterns

### Engine-Worker Separation
- **UI Layer (Passive):** The GUI (e.g., PySide6) should be responsible only for user input, display, and signal routing. It must not contain business logic.
- **Logic Engines (Pure):** Business logic should reside in "Engine" classes that are stateless. They should take inputs, perform calculations/transformations, and return results without side effects.
- **Worker Layer (Active):** Heavy I/O-bound tasks (scanning, networking) should run in `QThread`. Heavy CPU-bound or blocking OS tasks (file manipulation, complex processing) should run in a `ProcessPoolExecutor`.

### Signal-Driven Communication
- Components should be decoupled using signals and slots.
- Workers should emit signals to update the UI, rather than having direct references to UI widgets.
- This allows for easier unit testing and prevents threading violations.

## 2. Robustness & User Experience

### Proactive Error Handling
- **The "Dry Run" First Principle:** Never perform destructive operations without first calculating and showing the final outcome to the user.
- **Pre-flight Checks:** Perform permission and collision checks during the "discovery" or "preview" phase. Do not wait until the "execute" button is clicked to find out an operation will fail.
- **Graceful Cancellations:** Always account for "Cancel" actions in dialogs. Never assume a dialog will return a valid path or selection.

### Reactive Feedback
- Provide a dedicated, thread-safe console or status bar for real-time logging.
- The UI must remain responsive during all background operations.

## 3. Testability & Quality Assurance

### Design for Testability
- **Dependency Injection:** Pass dependencies (models, engines, scanners) into class constructors. This allows for easy injection of mocks during testing.
- **Mocking over Integration:** Prioritize unit tests that mock external systems (filesystems, networks, UI components) to verify logic in isolation.

### Documentation as Code
- Maintain a living `ARCHITECTURE.md` to describe system flow and a `API_REFERENCE.md` to document internal classes/methods.
- These documents serve as the source of truth for both human developers and AI assistants.

## 4. Implementation Standards

### Namespace Consistency
- Use package-level namespacing for all internal imports (e.g., `from batchalchemy.utils import logger`).
- Ensure standard entry points (e.g., `pyproject.toml` or `setup.py`) are configured for standard distribution (e.g., `uv`, `pipx`).

### Clean Code
- Follow established patterns for the specific language (e.g., PEP 8 for Python).
- Minimize output tokens in the AI response to keep the conversation focused.
- Avoid unnecessary preamble or postamble in code explanations.
