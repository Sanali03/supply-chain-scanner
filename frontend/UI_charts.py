from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class RiskChart(QWidget):
    def __init__(self, dependencies):
        super().__init__()
        layout = QVBoxLayout()

        # Count risks
        risk_counts = {"Critical":0, "High":0, "Medium":0, "Low":0, "Informational":0}
        for dep in dependencies:
            risk_counts[dep["risk"]] = risk_counts.get(dep["risk"], 0) + 1

        # Create pie chart
        fig, ax = plt.subplots()
        labels = list(risk_counts.keys())
        sizes = list(risk_counts.values())
        colors = ["red", "orange", "yellow", "green", "blue"]

        ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors)
        ax.set_title("Dependency Risk Distribution")

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.setLayout(layout)
