from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt


class ScanHistoryTable(QWidget):
    def __init__(self, history):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ===== Title =====
        title = QLabel("Scan History")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Date", "Project", "Dependencies", "Vulnerabilities"
        ])

        # 🔥 UI IMPROVEMENTS
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Stretch columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Hide row numbers
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.update_data(history)

    # ============================
    # UPDATE DATA
    # ============================

    def update_data(self, history):
        self.table.setRowCount(0)

        for scan in history:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Date
            self.table.setItem(row, 0, QTableWidgetItem(scan.get("date", "")))

            # Project
            project_item = QTableWidgetItem(scan.get("project", ""))
            project_item.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            self.table.setItem(row, 1, project_item)

            # Dependencies count
            deps = scan.get("deps", 0)
            deps_item = QTableWidgetItem(str(deps))
            deps_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Color based on size
            if deps > 50:
                deps_item.setForeground(QColor("#f97316"))  # orange
            else:
                deps_item.setForeground(QColor("#22c55e"))  # green

            self.table.setItem(row, 2, deps_item)

            # Vulnerabilities count
            vulns = scan.get("vulns", 0)
            vulns_item = QTableWidgetItem(str(vulns))
            vulns_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Color based on severity
            if vulns > 20:
                vulns_item.setForeground(QColor("#dc2626"))  # red
            elif vulns > 5:
                vulns_item.setForeground(QColor("#f97316"))  # orange
            else:
                vulns_item.setForeground(QColor("#22c55e"))  # green

            vulns_item.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

            self.table.setItem(row, 3, vulns_item)

        self.table.resizeColumnsToContents()