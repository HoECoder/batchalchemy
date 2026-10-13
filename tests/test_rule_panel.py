import pytest
from unittest.mock import MagicMock
from batchalchemy.views.widgets.rule_panel import RulePanel
from batchalchemy.workers.rule_engine import RuleEngine

def test_rule_panel_apply():
    mock_callback = MagicMock()
    
    panel = RulePanel(mock_callback)
    
    # Simulate inputs
    panel.search_input.setText("test")
    panel.replace_input.setText("replace")
    panel.regex_pattern.setText(".*")
    panel.regex_replace.setText("replaced")
    panel.prefix_input.setText("pre_")
    panel.suffix_input.setText("_post")
    
    panel.handle_apply()
    
    mock_callback.assert_called_once()
    engine = mock_callback.call_args[0][0]
    assert isinstance(engine, RuleEngine)
    assert engine.rules[0]["type"] == "search_replace"
    assert engine.rules[1]["type"] == "regex"
    assert engine.rules[2]["type"] == "prefix"
    assert engine.rules[3]["type"] == "suffix"
