from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class DependencyTable(QWidget):
    def __init__(self, dependencies):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableWidget(len(dependencies), 4)
        self.table.setHorizontalHeaderLabels(["Name", "Version", "Risk", "Vendor"])

        for row, dep in enumerate(dependencies):
            self.table.setItem(row, 0, QTableWidgetItem(dep["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(dep["version"]))
            self.table.setItem(row, 2, QTableWidgetItem(dep["risk"]))
            self.table.setItem(row, 3, QTableWidgetItem(dep["vendor"]))

        layout.addWidget(self.table)
        self.setLayout(layout)
