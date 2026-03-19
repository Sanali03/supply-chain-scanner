from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Supply Chain Scanner")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20pt; font-weight: bold; color: #3498db;")

        # Subtitle
        subtitle = QLabel("Upload your SBOM file to begin scanning")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 12pt; color: #2c3e50;")

        # Upload button
        upload_btn = QPushButton("Import File")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 12pt;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        upload_btn.clicked.connect(self.open_file_dialog)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select SBOM File", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            print(f"User uploaded file: {file_name}")
            # Later: trigger backend scan here
