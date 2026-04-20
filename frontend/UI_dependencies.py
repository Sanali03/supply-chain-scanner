from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QSizePolicy
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt


class DependencyTable(QWidget):
    def __init__(self, dependencies):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ===== Title =====
        title = QLabel("Dependencies")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Name", "Version", "Risk", "Source"
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
        self.table.verticalHeader().setDefaultSectionSize(50)

        # Clean look
        self.table.verticalHeader().setVisible(False)

        # Stretch columns nicely
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Slightly bigger font for readability
        self.table.setFont(QFont("Segoe UI", 11))

        layout.addWidget(self.table, stretch=1)
        self.setLayout(layout)

        self.update_data(dependencies)

    # ============================
    # UPDATE DATA
    # ============================
    def update_data(self, dependencies):
        self.table.setRowCount(0)

        for dep in dependencies:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # ===== Name =====
            name_item = QTableWidgetItem(dep.get("name", ""))
            name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row, 0, name_item)

            # ===== Version =====
            version_item = QTableWidgetItem(dep.get("version", ""))
            self.table.setItem(row, 1, version_item)

            # ===== Risk =====
            risk = dep.get("risk", "UNKNOWN")
            if not risk or risk == "N/A":
                risk = "UNKNOWN"

            risk = risk.upper()
            risk_item = QTableWidgetItem(risk)

            # 🎨 Color coding
            color_map = {
                "CRITICAL": "#dc2626",
                "HIGH": "#ef4444",
                "MEDIUM": "#f59e0b",
                "LOW": "#22c55e",
                "UNKNOWN": "#94a3b8"
            }

            risk_item.setForeground(QColor(color_map.get(risk, "#94a3b8")))
            risk_item.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

            # Center align risk
            risk_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 2, risk_item)

            # ===== Source =====
            Source = dep.get("source") or dep.get("ecosystem", "Unknown")
            Source_item = QTableWidgetItem(Source)
            self.table.setItem(row, 3, Source_item)
