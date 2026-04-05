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

from backend.sbom_generator import generate_sbom
from backend.sbom_parser import parse_sbom
from backend.db_service import save_project_and_dependencies

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

        self.button = QPushButton("Upload & Scan Project")
        self.button.clicked.connect(self.upload_file)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def upload_file(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Project Folder"
        )

        if folder_path:
            folder_name = os.path.basename(folder_path)
            destination = os.path.join(UPLOAD_FOLDER, folder_name)

            if os.path.exists(destination):
                shutil.rmtree(destination)

            shutil.copytree(folder_path, destination)

            self.label.setText(f"Uploaded: {folder_name}\nScanning...")

            try:
                project_name = folder_name
                project_path = destination

                sbom_file = generate_sbom(project_path)

                if sbom_file:
                    dependencies = parse_sbom(sbom_file)
                    save_project_and_dependencies(
                        project_name,
                        project_path,
                        dependencies
                    )

                    self.label.setText(f"Scan completed: {folder_name}")
                else:
                    self.label.setText("Scan failed!")

            except Exception as e:
                self.label.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SupplyChainScanner()
    window.show()
    sys.exit(app.exec())