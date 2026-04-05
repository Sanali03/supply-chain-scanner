from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class DependencyTable(QWidget):
    def __init__(self, dependencies):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Dependencies")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Version", "Risk", "Vendor"])

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.update_data(dependencies)

    def update_data(self, dependencies):
        self.table.setRowCount(0)

        for dep in dependencies:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(dep.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(dep.get("version", "")))

            risk = dep.get("risk", "LOW")
            risk_item = QTableWidgetItem(risk)

            if risk.upper() == "CRITICAL":
                risk_item.setForeground(Qt.GlobalColor.red)
            elif risk.upper() == "HIGH":
                risk_item.setForeground(Qt.GlobalColor.darkRed)
            elif risk.upper() == "MEDIUM":
                risk_item.setForeground(Qt.GlobalColor.darkYellow)
            else:
                risk_item.setForeground(Qt.GlobalColor.darkGreen)
            
            risk_item.setForeground(Qt.GlobalColor.white)

            self.table.setItem(row, 2, risk_item)
            self.table.setItem(row, 3, QTableWidgetItem(dep.get("vendor", "PyPI")))

        self.table.resizeColumnsToContents()