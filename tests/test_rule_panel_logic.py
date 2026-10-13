import pytest
from unittest.mock import MagicMock, patch
from batchalchemy.views.widgets.rule_panel import RulePanel
from batchalchemy.workers.rule_engine import RuleEngine

def test_rule_panel_input_collection():
    mock_callback = MagicMock()
    
    # We don't need to mock RuleEngine here since we want to test the actual collection
    panel = RulePanel(mock_callback)
    
    # Simulate inputs
    panel.search_input.setText("search_str")
    panel.replace_input.setText("replace_str")
    panel.regex_pattern.setText(".*")
    panel.regex_replace.setText("replaced")
    panel.prefix_input.setText("prefix_")
    panel.suffix_input.setText("_suffix")
    
    panel.handle_apply()
    
    mock_callback.assert_called_once()
    engine = mock_callback.call_args[0][0]
    assert engine.rules[0]["type"] == "search_replace"
    assert engine.rules[1]["type"] == "regex"
    assert engine.rules[2]["type"] == "prefix"
    assert engine.rules[3]["type"] == "suffix"
