from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QSizePolicy
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt


class VulnerabilityTable(QWidget):
    def __init__(self, vulnerabilities):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ===== Title =====
        title = QLabel("Vulnerabilities")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "CVE ID", "Severity", "Package", "Description"
        ])

        # ===== UI IMPROVEMENTS =====
        self.table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Bigger rows
        self.table.verticalHeader().setDefaultSectionSize(60)

        # Clean look
        self.table.verticalHeader().setVisible(False)

        # Stretch columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Better readability
        self.table.setFont(QFont("Segoe UI", 11))

        layout.addWidget(self.table, stretch=1)
        self.setLayout(layout)

        self.update_data(vulnerabilities)

    # ============================
    # UPDATE DATA
    # ============================
    def update_data(self, vulnerabilities):
        self.table.setRowCount(0)

        for vuln in vulnerabilities:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # ===== CVE ID =====
            cve = vuln.get("cve") or "N/A"
            cve_item = QTableWidgetItem(cve)
            self.table.setItem(row, 0, cve_item)

            # ===== Severity (FIXED HANDLING) =====
            severity = vuln.get("severity")

            if not severity:
                severity = "UNKNOWN"

            severity = severity.upper()
            sev_item = QTableWidgetItem(severity)

            # 🎨 Color mapping (consistent with dashboard)
            color_map = {
                "CRITICAL": "#dc2626",
                "HIGH": "#ef4444",
                "MEDIUM": "#f59e0b",
                "LOW": "#22c55e",
                "UNKNOWN": "#94a3b8"
            }

            sev_item.setForeground(QColor(color_map.get(severity, "#94a3b8")))
            sev_item.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

            # Center align severity
            sev_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 1, sev_item)

            # ===== Package =====
            package = vuln.get("package", "")
            pkg_item = QTableWidgetItem(package)
            self.table.setItem(row, 2, pkg_item)

            # ===== Description (WRAPPED + CLEAN) =====
            description = vuln.get("description") or "No description available"
            desc_item = QTableWidgetItem(description)

            desc_item.setTextAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )

            self.table.setItem(row, 3, desc_item)

        # Enable word wrap for long descriptions
        self.table.setWordWrap(True)
