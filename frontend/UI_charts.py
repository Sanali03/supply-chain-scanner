from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class RiskChart(QWidget):
    def __init__(self, dependencies=None, vulnerabilities=None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)

        self.animation = None  # keep reference

        self.update_chart(dependencies or [], vulnerabilities or [])

    # ============================
    # UPDATE CHART WITH ANIMATION
    # ============================
    def update_chart(self, dependencies, vulnerabilities):
        self.ax.clear()

        total_deps = len(dependencies)

    # Get unique vulnerable packages
        vulnerable_packages = set()
        for vuln in vulnerabilities:
            pkg = vuln.get("package")
            if pkg:
                vulnerable_packages.add(pkg)

        vulnerable_count = len(vulnerable_packages)
        safe_count = max(total_deps - vulnerable_count, 0)

    # ============================
    # HANDLE EMPTY / ZERO CASE
    # ============================
        if total_deps == 0 or (safe_count == 0 and vulnerable_count == 0):
            self.ax.text(
                0.5, 0.5,
                "No Data Available",
                ha='center',
                va='center',
                fontsize=14,
                color="white"
            )

            self.figure.patch.set_facecolor("#1e293b")
            self.ax.set_facecolor("#1e293b")
            self.canvas.draw()
            return

        labels = ["Safe", "Vulnerable"]
        sizes = [safe_count, vulnerable_count]
        colors = ["#22c55e", "#ef4444"]

        # ============================
        # ANIMATION FIX (SAFE)
        # ============================
        from matplotlib.animation import FuncAnimation

        frames = 20

        def animate(frame):
            self.ax.clear()

            # Avoid zero division
            animated_sizes = [s * frame / frames for s in sizes]

            # If all values are 0 → skip drawing
            if sum(animated_sizes) == 0:
                return

            wedges, texts, autotexts = self.ax.pie(
                animated_sizes,
                labels=labels,
                colors=colors,
                startangle=90,
                autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
                pctdistance=0.75,
                textprops={"color": "white", "fontsize": 11}
            )

            # Donut hole
            centre_circle = plt.Circle((0, 0), 0.65, fc="#1e293b")
            self.ax.add_artist(centre_circle)

            # Center text (total deps)
            self.ax.text(
                0, 0,
                f"{total_deps}\nDependencies",
                ha="center",
                va="center",
                color="white",
                fontsize=13,
                fontweight="bold"
            )

            self.ax.set_title(
                "Dependency Security Overview",
                color="white",
                fontsize=14,
                fontweight="bold"
            )

        self.anim = FuncAnimation(
            self.figure,
            animate,
            frames=frames,
            interval=30,
            repeat=False
        )

        # Styling
        self.figure.patch.set_facecolor("#1e293b")
        self.ax.set_facecolor("#1e293b")

        self.canvas.draw()