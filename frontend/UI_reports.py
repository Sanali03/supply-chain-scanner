from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class ReportViewer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setText(
            "SBOM Process Documentation:\n\n"
            "- Syft used for SBOM parsing\n"
            "- Dependencies stored in SQLite\n"
            "- Risks classified by CVSS\n"
            "- Vulnerabilities fetched via OSV API\n"
        )
        layout.addWidget(self.text_area)
        self.setLayout(layout)
