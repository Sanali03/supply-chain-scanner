from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class DependencyTable(QWidget):
    def __init__(self, dependencies):
        super().__init__()
        self.setStyleSheet("background-color: #1a1f3a;")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel(" Dependencies")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #3498db;")
        layout.addWidget(title)
        
        self.table = QTableWidget(len(dependencies), 4)
        self.table.setHorizontalHeaderLabels(["Name", "Version", "Risk", "Vendor"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2d3561;
                gridline-color: #3d4661;
                border: none;
            }
            QTableWidget::item {
                color: #ecf0f1;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        for row, dep in enumerate(dependencies):
            self.table.setItem(row, 0, QTableWidgetItem(dep["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(dep["version"]))
            risk_item = QTableWidgetItem(dep["risk"])
            # Color code risk levels
            if dep["risk"] == "High":
                risk_item.setForeground(Qt.GlobalColor.red)
            elif dep["risk"] == "Medium":
                risk_item.setForeground(Qt.GlobalColor.yellow)
            else:
                risk_item.setForeground(Qt.GlobalColor.green)
            self.table.setItem(row, 2, risk_item)
            self.table.setItem(row, 3, QTableWidgetItem(dep["vendor"]))

        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)
        self.setLayout(layout)
