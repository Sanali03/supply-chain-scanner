from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from UI_policy_status import PolicyDetailsWidget
from UI_trend_chart import TrendChart
from PyQt6.QtCore import Qt, pyqtSignal


class HomePage(QWidget):
    
    upload_requested = pyqtSignal()

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

        # ================= MAIN CONTENT (FIXED) =================
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)

        # ===== LEFT SIDE (Policy + Table) =====
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        # ---- POLICY ----
        policy_frame = QFrame()
        policy_frame.setObjectName("card")
        policy_layout = QVBoxLayout(policy_frame)

        self.policy_widget = PolicyDetailsWidget()
        policy_layout.addWidget(self.policy_widget)

        # ---- TABLE ----
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

        # Add to LEFT column
        left_layout.addWidget(policy_frame)
        left_layout.addWidget(self.table)

        # ===== RIGHT SIDE (TREND CHART) =====
        self.trend_chart = TrendChart()

        chart_card = QFrame()
        chart_card.setObjectName("card")

        chart_layout = QVBoxLayout()
        chart_layout.setSpacing(10)

        chart_title = QLabel("Scan Trend")
        chart_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        chart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.trend_chart)

        chart_card.setLayout(chart_layout)

        # Make chart fill full height
        chart_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add to main layout
        content_layout.addLayout(left_layout, 2)
        content_layout.addWidget(chart_card, 3)

        self.main_layout.addLayout(content_layout)

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

        dep_count = len(dependencies)
        vuln_count = len(vulnerabilities)

        total_scans = len(full_history)

        project_scans = [
            h for h in full_history if h["project"] == current_project_name
        ]

        latest_scan = project_scans[0] if project_scans else {}

        risk = latest_scan.get("status", "UNKNOWN").upper()

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

        self.dep_value["label"].setText(str(dep_count))
        self.vuln_value["label"].setText(str(vuln_count))
        self.scan_value["label"].setText(str(total_scans))

        self.risk_value["label"].setText(risk)
        self.risk_value["label"].setStyleSheet(f"color: {color};")

        # ===== TABLE =====
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

        # ===== POLICY =====
        if latest_scan and "policy_enforcement" in latest_scan:
            self.policy_widget.update_policy_info(latest_scan["policy_enforcement"])
        else:
            self.policy_widget.update_policy_info({
                "status": "pending-scan",
                "reason": "Run a scan to evaluate security policies."
            })

        # ===== TREND =====
        self.trend_chart.update_chart(project_scans)

    # ================= FILE PICKER =================
    def open_folder_dialog(self):
        self.upload_requested.emit()