from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from datetime import datetime


class TrendChart(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)

        self.apply_dark_theme()

    def apply_dark_theme(self):
        self.figure.patch.set_facecolor("#1e293b")
        self.ax.set_facecolor("#1e293b")

    def update_chart(self, history):
        self.ax.clear()
        self.apply_dark_theme()

        if not history:
            self.ax.text(0.5, 0.5, "No Scan Data",
                         ha='center', va='center',
                         color="white", fontsize=14)
            self.canvas.draw()
            return

        # ✅ FIX 1: SORT DATA (IMPORTANT)
        history = sorted(
            history,
            key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S")
        )

        # Extract data
        dates = []
        vuln_counts = []

        for scan in history:
            dt = datetime.strptime(scan['date'], "%Y-%m-%d %H:%M:%S")
            dates.append(dt)

            # ✅ FIX 2: CORRECT KEY
            vuln_counts.append(scan.get("vulns", 0))

        # Plot
        self.ax.plot(
            dates,
            vuln_counts,
            marker='o',
            linewidth=2,
            color="#38bdf8"
        )

        self.ax.set_title("Vulnerability Trend Over Time",
                          color="white", fontsize=14, fontweight="bold")

        self.ax.tick_params(axis='x', colors='white', rotation=30)
        self.ax.tick_params(axis='y', colors='white')

        self.ax.grid(color="#334155", linestyle='--', linewidth=0.5)

        # ✅ FIX 3: MAKE CHANGES VISIBLE
        self.ax.set_ylim(bottom=0)
        self.ax.margins(y=0.2)

        self.figure.tight_layout()

        self.canvas.draw()
