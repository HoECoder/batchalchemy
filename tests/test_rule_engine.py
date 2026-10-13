import pytest
from batchalchemy.workers.rule_engine import RuleEngine

def test_search_replace_rule():
    engine = RuleEngine()
    engine.add_search_replace("old_text", "new_text")
    filenames = ["old_text_file.txt", "another_file.txt", "old_text.png"]
    results = engine.apply_rules(filenames)
    assert results == ["new_text_file.txt", "another_file.txt", "new_text.png"]

def test_regex_rule():
    engine = RuleEngine()
    # Replace digits with X
    engine.add_regex(r"\d+", "X")
    filenames = ["file123.txt", "image_45.png", "no_numbers.jpg"]
    results = engine.apply_rules(filenames)
    assert results == ["fileX.txt", "image_X.png", "no_numbers.jpg"]

def test_prefix_rule():
    engine = RuleEngine()
    engine.add_prefix("PROD_")
    filenames = ["data.csv", "logs.txt"]
    results = engine.apply_rules(filenames)
    assert results == ["PROD_data.csv", "PROD_logs.txt"]

def test_suffix_rule():
    engine = RuleEngine()
    engine.add_suffix("_v1")
    filenames = ["test.py", "script.sh"]
    results = engine.apply_rules(filenames)
    assert results == ["test_v1.py", "script_v1.sh"]

def test_multiple_rules():
    engine = RuleEngine()
    engine.add_prefix("FINAL_")
    engine.add_suffix("_v1")
    engine.add_search_replace("test", "prod")
    filenames = ["test_file.txt"]
    results = engine.apply_rules(filenames)
    assert results == ["FINAL_prod_file_v1.txt"]

def test_invalid_regex_handling():
    engine = RuleEngine()
    engine.add_regex("[unclosed-bracket", "X")
    filenames = ["file.txt"]
    # Should handle gracefully (not crash)
    results = engine.apply_rules(filenames)
    assert results == ["file.txt"]

def test_no_rules():
    engine = RuleEngine()
    filenames = ["file.txt"]
    assert engine.apply_rules(filenames) == ["file.txt"]

def test_empty_inputs():
    engine = RuleEngine()
    assert engine.apply_rules([]) == []

def test_complex_rule_chain():
    engine = RuleEngine()
    engine.add_search_replace("A", "B")
    engine.add_prefix("C")
    engine.add_suffix(".D")
    filenames = ["A_file"]
    results = engine.apply_rules(filenames)
    assert results == ["CB_file.D"]
