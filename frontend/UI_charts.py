from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class RiskChart(QWidget):
    def __init__(self, dependencies=None, vulnerabilities=None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)

        # Initial plot
        self.update_chart(dependencies or [], vulnerabilities or [])

    # ============================
    # UPDATE CHART (FINAL VERSION)
    # ============================
    def update_chart(self, dependencies, vulnerabilities):
        self.ax.clear()

        # ============================
        # CALCULATE SAFE vs VULNERABLE
        # ============================
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
        # DATA FOR CHART
        # ============================
        labels = ["Safe", "Vulnerable"]
        sizes = [safe_count, vulnerable_count]
        colors = ["#22c55e", "#ef4444"]  # green / red

        # ============================
        # HANDLE EMPTY DATA
        # ============================
        if total_deps == 0:
            self.ax.text(
                0.5, 0.5,
                "No Data Available",
                ha='center',
                va='center',
                fontsize=14,
                color="white"
            )
        else:
            self.ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                colors=colors,
                startangle=90,
                textprops={"color": "white", "fontsize": 11}
            )

        # ============================
        # STYLING
        # ============================
        self.figure.patch.set_facecolor("#1e293b")
        self.ax.set_facecolor("#1e293b")

        self.ax.set_title(
            "Dependency Security Overview",
            color="white",
            fontsize=14,
            fontweight="bold"
        )

        self.canvas.draw()
