from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
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
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))

        self.btn = QPushButton("Browse Folder")
        self.btn.setObjectName("primaryButton")
        self.btn.clicked.connect(self.open_folder_dialog)

        upload_layout.addWidget(title)
        upload_layout.addWidget(self.btn)

        upload.setLayout(upload_layout)
        self.main_layout.addWidget(upload)

        # ================= STATS =================
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

        self.table.setHorizontalHeaderLabels([
            "Project", "Dependencies", "Vulnerabilities"
        ])

        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.table, stretch=1)

        self.setLayout(self.main_layout)

    # ================= STAT CARD =================
    def create_stat_card(self, title, color):
        frame = QFrame()
        frame.setObjectName("statCard")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_label = QLabel("0")
        value_label.setObjectName("statValue")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"color: {color};")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        frame.setLayout(layout)

        return {"frame": frame, "label": value_label}

    # ================= UPDATE DATA =================
    def update_summary(self, dependencies, vulnerabilities, full_history, current_project_name):

        # ===== COUNTS =====
        dep_count = len(dependencies)
        vuln_count = len(vulnerabilities)

        # ✅ TOTAL scans (ALL projects)
        total_scans = len(full_history)

        # ✅ FILTER scans of CURRENT project
        project_scans = [
            h for h in full_history if h["project"] == current_project_name
        ]

        # ✅ Latest scan for risk
        latest_scan = project_scans[0] if project_scans else {}

        risk = latest_scan.get("status", "UNKNOWN").upper()

        # ===== COLOR =====
        if risk == "CRITICAL":
            color = "#dc2626"
        elif risk == "HIGH":
            color = "#ef4444"
        elif risk == "MEDIUM":
            color = "#f59e0b"
        elif risk == "LOW":
            color = "#22c55e"
        else:
            color = "#94a3b8"

        # ===== UPDATE STATS =====
        self.dep_value["label"].setText(str(dep_count))
        self.vuln_value["label"].setText(str(vuln_count))
        self.scan_value["label"].setText(str(total_scans))

        self.risk_value["label"].setText(risk)
        self.risk_value["label"].setStyleSheet(f"color: {color};")

        # ===== UPDATE TABLE =====
        self.table.setRowCount(0)

        for row, scan in enumerate(project_scans):
            self.table.insertRow(row)

            project_item = QTableWidgetItem(scan.get("project", ""))
            deps_item = QTableWidgetItem(str(scan.get("deps", 0)))
            vulns_item = QTableWidgetItem(str(scan.get("vulns", 0)))

            deps_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            vulns_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, project_item)
            self.table.setItem(row, 1, deps_item)
            self.table.setItem(row, 2, vulns_item)

    # ================= FILE PICKER =================
    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")

        if folder:
            parent = self.parent()
            if hasattr(parent, "upload_and_scan"):
                parent.upload_and_scan()
