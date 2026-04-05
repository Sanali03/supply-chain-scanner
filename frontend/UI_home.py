from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QFrame, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # ================= UPLOAD SECTION =================
        upload = QFrame()
        upload.setObjectName("card")

        upload_layout = QVBoxLayout()

        title = QLabel("Upload Project for Scan")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        self.btn = QPushButton("Browse Folder")
        self.btn.setObjectName("primaryButton")
        self.btn.clicked.connect(self.open_folder_dialog)

        upload_layout.addWidget(title)
        upload_layout.addWidget(self.btn)

        upload.setLayout(upload_layout)
        self.main_layout.addWidget(upload)

        # ================= STATS SECTION =================
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        self.dep_value = self.create_stat_card("Dependencies", "#38bdf8")
        self.vuln_value = self.create_stat_card("Vulnerabilities", "#f59e0b")
        self.scan_value = self.create_stat_card("Scans", "#a78bfa")
        self.risk_value = self.create_stat_card("Risk", "#22c55e")

        stats_layout.addWidget(self.dep_value["frame"])
        stats_layout.addWidget(self.vuln_value["frame"])
        stats_layout.addWidget(self.scan_value["frame"])
        stats_layout.addWidget(self.risk_value["frame"])

        self.main_layout.addLayout(stats_layout)

        # ================= TABLE =================
        self.table = QTableWidget(0, 3)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels(["Project", "Dependencies", "Vulnerabilities"])

        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)

    # ================= STAT CARD =================
    def create_stat_card(self, title, color):
        frame = QFrame()
        frame.setObjectName("statCard")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")

        value_label = QLabel("0")
        value_label.setObjectName("statValue")
        value_label.setStyleSheet(f"color: {color};")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        frame.setLayout(layout)

        return {"frame": frame, "label": value_label}

    # ================= UPDATE DATA =================
    def update_summary(self, dependencies, vulnerabilities, history):
        dep_count = len(dependencies)
        vuln_count = len(vulnerabilities)
        scan_count = len(history)

        # Risk logic
        if vuln_count == 0:
            risk = "LOW"
            color = "#22c55e"
        elif vuln_count < 5:
            risk = "MEDIUM"
            color = "#f59e0b"
        else:
            risk = "HIGH"
            color = "#ef4444"

        # Update values
        self.dep_value["label"].setText(str(dep_count))
        self.vuln_value["label"].setText(str(vuln_count))
        self.scan_value["label"].setText(str(scan_count))
        self.risk_value["label"].setText(risk)
        self.risk_value["label"].setStyleSheet(f"color: {color};")

        # Update table
        self.table.setRowCount(0)

        for row, scan in enumerate(history):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(scan.get("project", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(scan.get("deps", 0))))
            self.table.setItem(row, 2, QTableWidgetItem(str(scan.get("vulns", 0))))

    # ================= FILE PICKER =================
    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")

        if folder:
            parent = self.parent()
            if hasattr(parent, "upload_and_scan"):
                parent.upload_and_scan()
