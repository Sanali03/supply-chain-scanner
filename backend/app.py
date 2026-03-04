import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class SupplyChainScanner(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Supply Chain Scanner")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("No file selected")
        layout.addWidget(self.label)

        self.button = QPushButton("Upload Project")
        self.button.clicked.connect(self.upload_file)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Files (*)"
        )

        if file_path:
            filename = os.path.basename(file_path)
            destination = os.path.join(UPLOAD_FOLDER, filename)

            shutil.copy(file_path, destination)

            self.label.setText(f"Uploaded: {filename}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SupplyChainScanner()
    window.show()
    sys.exit(app.exec())