from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class RiskChart(QWidget):
    def __init__(self, dependencies):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)

        # Initial plot
        self.update_chart(dependencies)

    # ============================
    # UPDATE CHART (FIXED)
    # ============================

    def update_chart(self, dependencies):
        self.ax.clear()

        # Risk categories
        risk_counts = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Informational": 0
        }

        # Count risks safely
        for dep in dependencies:
            risk = dep.get("risk", "Low")
            risk_counts[risk] = risk_counts.get(risk, 0) + 1

        labels = []
        sizes = []
        colors = []

        # 🎨 COLOR MAPPING (THIS IS WHERE COLORS GO)
        color_map = {
            "Critical": "#e74c3c",     # red
            "High": "#e67e22",         # orange
            "Medium": "#f1c40f",       # yellow
            "Low": "#2ecc71",          # green
            "Informational": "#3498db" # blue
        }

        for key, value in risk_counts.items():
            if value > 0:
                labels.append(key)
                sizes.append(value)
                colors.append(color_map.get(key, "#95a5a6"))

        # Handle empty data
        if not sizes:
            self.ax.text(
                0.5, 0.5,
                "No Data Available",
                ha='center',
                va='center',
                fontsize=12,
                color="white"
            )
        else:
            self.ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                colors=colors
            )

        # Dark theme background
        self.figure.patch.set_facecolor("#1a1f3a")
        self.ax.set_facecolor("#1a1f3a")

        self.ax.set_title("Dependency Risk Distribution", color="white")

        self.canvas.draw()
