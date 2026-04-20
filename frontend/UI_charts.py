from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from collections import Counter


class RiskChart(QWidget):
    def __init__(self, dependencies=None, vulnerabilities=None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # ===== GRID LAYOUT =====
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

        # Create figures
        self.fig1, self.ax1 = plt.subplots()
        self.fig2, self.ax2 = plt.subplots()
        self.fig3, self.ax3 = plt.subplots()
        self.fig4, self.ax4 = plt.subplots()

        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas3 = FigureCanvas(self.fig3)
        self.canvas4 = FigureCanvas(self.fig4)

        # Add to grid
        self.grid.addWidget(self.canvas1, 0, 0)
        self.grid.addWidget(self.canvas2, 0, 1)
        self.grid.addWidget(self.canvas3, 1, 0)
        self.grid.addWidget(self.canvas4, 1, 1)

        self.update_chart(dependencies or [], vulnerabilities or [])

    # ============================
    # MAIN UPDATE
    # ============================
    def update_chart(self, dependencies, vulnerabilities):
        self.plot_severity_donut(vulnerabilities)
        self.plot_top_packages(vulnerabilities)
        self.plot_risk_card(vulnerabilities)
        self.plot_ecosystem_chart(dependencies, vulnerabilities)

    # ============================
    # 1. SEVERITY DONUT (FIXED)
    # ============================
    def plot_severity_donut(self, vulnerabilities):
        self.ax1.clear()

        severity_count = Counter()

        for v in vulnerabilities:
            sev = v.get("severity", "LOW").upper()
            if sev == "MODERATE":
                sev = "MEDIUM"
            severity_count[sev] += 1

        # WEIGHTED
        weight_map = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        labels, sizes, colors = [], [], []

        color_map = {
            "CRITICAL": "#dc2626",
            "HIGH": "#f97316",
            "MEDIUM": "#f59e0b",
            "LOW": "#22c55e"
        }

        for k in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if severity_count[k]:
                labels.append(f"{k} ({severity_count[k]})")
                sizes.append(severity_count[k] * weight_map[k])  # 🔥 FIX
                colors.append(color_map[k])

        if not sizes:
            self.ax1.text(0.5, 0.5, "No Data", ha="center", color="white")
            return

        wedges, texts, autotexts = self.ax1.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"color": "white"}
        )

        for t in texts:
            t.set_color("white")
        for t in autotexts:
            t.set_color("white")

        # Donut center
        centre = plt.Circle((0, 0), 0.6, fc="#1e293b")
        self.ax1.add_artist(centre)

        self.ax1.set_title("Risk Distribution (Weighted)", color="white")

        self.fig1.patch.set_facecolor("#1e293b")
        self.ax1.set_facecolor("#1e293b")

        self.canvas1.draw()

    # ============================
    # 2. TOP PACKAGES (FIXED)
    # ============================
    def plot_top_packages(self, vulnerabilities):
        self.ax2.clear()

        from collections import Counter

        package_count = Counter(v.get("package", "Unknown") for v in vulnerabilities)
        top = package_count.most_common(5)

        if not top:
            self.ax2.text(0.5, 0.5, "No Data", ha="center", va="center", color="white")
            return

        names = [x[0] for x in top]
        counts = [x[1] for x in top]

        names.reverse()
        counts.reverse()

        colors = ["#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe", "#dbeafe"][:len(names)]

        bars = self.ax2.barh(names, counts, color=colors, height=0.5)

        # ADD VALUE LABELS
        for bar in bars:
            width = bar.get_width()
            self.ax2.text(
                width + 0.5,
                bar.get_y() + bar.get_height() / 2,
                f"{int(width)}",
                va='center',
                color="white",
                fontsize=10
            )

        # STYLING
        self.ax2.set_title("Top Vulnerable Packages", color="white", fontsize=13, pad=10)

        self.ax2.tick_params(axis='x', colors='white')
        self.ax2.tick_params(axis='y', colors='white')

        # Remove spines (clean look)
        for spine in self.ax2.spines.values():
            spine.set_visible(False)
    
        # Subtle grid (x-axis only)
        self.ax2.grid(axis='x', linestyle='--', alpha=0.2)

        # Remove extra padding
        self.ax2.margins(y=0.15)

        # Background
        self.fig2.patch.set_facecolor("#1e293b")
        self.ax2.set_facecolor("#1e293b")

        # Tight layout = no clipping
        self.fig2.tight_layout()

        self.canvas2.draw()

    # ============================
    # 3. REAL RISK CARD
    # ============================
    def plot_risk_card(self, vulnerabilities):
        self.ax3.clear()

        from backend.risk_calculator import calculate_risk

        # ✅ Use your REAL backend logic
        score, status = calculate_risk(vulnerabilities)

        color_map = {
            "LOW": "#22c55e",
            "MEDIUM": "#f59e0b",
            "HIGH": "#f97316",
            "CRITICAL": "#dc2626"
        }

        color = color_map.get(status, "#22c55e")

        # DRAW CARD
        self.ax3.axis("off")

        self.ax3.text(
            0.5, 0.6,
            f"{score:.1f}",
            ha="center",
            va="center",
            fontsize=36,
            fontweight="bold",
            color="white"
        )

        self.ax3.text(
            0.5, 0.4,
            f"{status} RISK",
            ha="center",
            va="center",
            fontsize=16,
            fontweight="bold",
            color=color
        )

        self.ax3.text(
            0.5, 0.85,
            "Risk Score",
            ha="center",
            fontsize=14,
            color="white"
        )

        self.fig3.patch.set_facecolor("#1e293b")
        self.ax3.set_facecolor("#1e293b")

        self.canvas3.draw()
    # ============================
    # 4. ECOSYSTEM + RATIO
    # ============================
    def plot_ecosystem_chart(self, dependencies, vulnerabilities):
        self.ax4.clear()

        total_deps = len(dependencies)

        vulnerable_packages = set(v.get("package") for v in vulnerabilities if v.get("package"))
        vulnerable_count = len(vulnerable_packages)
        safe_count = max(total_deps - vulnerable_count, 0)

        # RATIO PIE (BETTER)
        labels = ["Safe", "Vulnerable"]
        sizes = [safe_count, vulnerable_count]
        colors = ["#22c55e", "#ef4444"]

        if total_deps == 0:
            self.ax4.text(0.5, 0.5, "No Data", ha="center", color="white")
            return

        wedges, texts, autotexts = self.ax4.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            textprops={"color": "white"}
        )

        for t in texts:
            t.set_color("white")
        for t in autotexts:
            t.set_color("white")

        self.ax4.set_title(
            f"Dependency Risk Ratio\n{vulnerable_count}/{total_deps} Vulnerable",
            color="white",
            pad=18
        )

        self.fig4.tight_layout(pad=3)

        self.ax4.set_facecolor("#1e293b")
        self.fig4.patch.set_facecolor("#1e293b")

        self.canvas4.draw()