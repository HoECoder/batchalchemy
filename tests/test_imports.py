import pytest
import importlib
import logging

# Configure logging to see issues during import
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_import_all_modules():
    modules = [
        "batchalchemy.main",
        "batchalchemy.models.file_model",
        "batchalchemy.views.main_window",
        "batchalchemy.views.widgets.log_console",
        "batchalchemy.views.widgets.rule_panel",
        "batchalchemy.workers.scanner",
        "batchalchemy.workers.rename_task",
        "batchalchemy.workers.rule_engine",
        "batchalchemy.utils.logger",
    ]
    
    for module_path in modules:
        try:
            importlib.import_module(module_path)
        except ImportError as e:
            pytest.fail(f"Failed to import {module_path}: {e}")

def test_dependency_imports():
    # Check core dependencies
    import PySide6
    import os
    import re
    import concurrent.futures
    import threading
    import json
    import copy
    import sys
    import time
