import re
import os
from typing import List

class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_search_replace(self, search: str, replace: str):
        if search:
            self.rules.append({"type": "search_replace", "search": search, "replace": replace})

    def add_regex(self, pattern: str, replace: str):
        if pattern:
            self.rules.append({"type": "regex", "pattern": pattern, "replace": replace})

    def add_prefix(self, prefix: str):
        if prefix:
            self.rules.append({"type": "prefix", "value": prefix})

    def add_suffix(self, suffix: str):
        if suffix:
            self.rules.append({"type": "suffix", "value": suffix})

    def apply_rules(self, filenames: List[str]) -> List[str]:
        new_filenames = []
        for name in filenames:
            current_name = name
            for rule in self.rules:
                if rule["type"] == "search_replace":
                    current_name = current_name.replace(rule["search"], rule["replace"])
                elif rule["type"] == "regex":
                    try:
                        current_name = re.sub(rule["pattern"], rule["replace"], current_name)
                    except re.error:
                        pass
                elif rule["type"] == "prefix":
                    current_name = rule["value"] + current_name
                elif rule["type"] == "suffix":
                    base, ext = os.path.splitext(current_name)
                    current_name = f"{base}{rule['value']}{ext}"
            new_filenames.append(current_name)
        return new_filenames
