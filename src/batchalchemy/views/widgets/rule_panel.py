from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from batchalchemy.workers.rule_engine import RuleEngine

class RulePanel(QWidget):
    def __init__(self, apply_callback, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.engine = RuleEngine()
        self.apply_callback = apply_callback

        self.layout.addWidget(QLabel("Search & Replace"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search string...")
        self.layout.addWidget(self.search_input)
        
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace string...")
        self.layout.addWidget(self.replace_input)

        self.layout.addWidget(QLabel("Regex (Optional)"))
        self.regex_pattern = QLineEdit()
        self.regex_pattern.setPlaceholderText("Pattern...")
        self.layout.addWidget(self.regex_pattern)
        
        self.regex_replace = QLineEdit()
        self.regex_replace.setPlaceholderText("Replace...")
        self.layout.addWidget(self.regex_replace)

        self.layout.addWidget(QLabel("Prefix/Suffix"))
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Prefix...")
        self.layout.addWidget(self.prefix_input)
        
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("Suffix...")
        self.layout.addWidget(self.suffix_input)

        self.apply_btn = QPushButton("Apply Rules")
        self.apply_btn.clicked.connect(self.handle_apply)
        self.layout.addWidget(self.apply_btn)

    def handle_apply(self):
        rules = self.get_rules()
        self.apply_callback(rules)

    def get_rules(self):
        self.engine = RuleEngine()
        if self.search_input.text():
            self.engine.add_search_replace(self.search_input.text(), self.replace_input.text())
        if self.regex_pattern.text():
            self.engine.add_regex(self.regex_pattern.text(), self.regex_replace.text())
        if self.prefix_input.text():
            self.engine.add_prefix(self.prefix_input.text())
        if self.suffix_input.text():
            self.engine.add_suffix(self.suffix_input.text())
        return self.engine
