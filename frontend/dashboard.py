import sys
import os

# Ensure backend is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QMovie

# UI Components
from UI_dependencies import DependencyTable
from UI_vulnerabilities import VulnerabilityTable
from UI_reports import ReportViewer
from UI_charts import RiskChart
from UI_scan_history import ScanHistoryTable
from UI_home import HomePage

# Backend
from backend.backend_service import run_scan
from backend.db_service import get_dependencies, get_vulnerabilities, get_scan_history


# ============================
# THREAD WORKER
# ============================

class ScanWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, project_name, project_path):
        super().__init__()
        self.project_name = project_name
        self.project_path = project_path

    def run(self):
        try:
            run_scan(self.project_name, self.project_path)
        except Exception as e:
            print(f"❌ Scan error: {e}")
        self.finished.emit()


# ============================
# DASHBOARD
# ============================

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Supply Chain Scanner Dashboard")
        self.resize(1400, 800)

        # ================= MAIN LAYOUT =================
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ================= LOADER =================
        self.loader = QLabel(self)
        self.loader.setFixedSize(50, 50)

        movie = QMovie("spinner.gif")  # make sure file exists
        self.loader.setMovie(movie)
        movie.start()

        self.loader.setVisible(False) #hidden by default

        # ================= SIDEBAR =================
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setMaximumWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)

        # Logo
        logo = QLabel("Supply Chain\nScanner")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        sidebar_layout.addWidget(logo)

        # Upload button
        scan_btn = QPushButton("📁 Upload Project")
        scan_btn.setObjectName("primaryButton")
        scan_btn.clicked.connect(self.upload_and_scan)
        sidebar_layout.addWidget(scan_btn)

        # Navigation buttons
        self.nav_buttons = []

        nav_buttons = [
            ("Home", 0),
            ("Dependencies", 1),
            ("Vulnerabilities", 2),
            ("Risk Chart", 3),
            ("Reports", 4),
            ("Scan History", 5),
        ]

        for text, idx in nav_buttons:
            btn = QPushButton(text)
            btn.setObjectName("navButton")

            # FIX lambda late binding issue
            btn.clicked.connect(lambda _, i=idx: self.switch_tab(i))

            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # ================= CONTENT =================
        content = QWidget()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()

        # Load initial data
        dependencies = get_dependencies()
        vulnerabilities = get_vulnerabilities()
        scan_history = get_scan_history()

        # Create tabs (STORE references!)
        self.home_tab = HomePage()
        self.dep_tab = DependencyTable(dependencies)
        self.vuln_tab = VulnerabilityTable(vulnerabilities)
        self.chart_tab = RiskChart(dependencies)
        self.report_tab = ReportViewer()
        self.history_tab = ScanHistoryTable(scan_history)

        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.dep_tab, "Dependencies")
        self.tabs.addTab(self.vuln_tab, "Vulnerabilities")
        self.tabs.addTab(self.chart_tab, "Risk Chart")
        self.tabs.addTab(self.report_tab, "Reports")
        self.tabs.addTab(self.history_tab, "Scan History")

        content_layout.addWidget(self.tabs)
        main_layout.addWidget(content)

        self.setCentralWidget(main_container)

        # Initial load
        self.refresh_data()

    # ============================
    # NAVIGATION
    # ============================

    def switch_tab(self, index):
        self.tabs.setCurrentIndex(index)

    # ============================
    # REFRESH UI
    # ============================

    def refresh_data(self):
        try:
            dependencies = get_dependencies()
            vulnerabilities = get_vulnerabilities()
            scan_history = get_scan_history()

            # Update all tabs safely
            if hasattr(self.dep_tab, "update_data"):
                self.dep_tab.update_data(dependencies)

            if hasattr(self.vuln_tab, "update_data"):
                self.vuln_tab.update_data(vulnerabilities)

            if hasattr(self.chart_tab, "update_chart"):
                self.chart_tab.update_chart(dependencies)

            if hasattr(self.history_tab, "update_data"):
                self.history_tab.update_data(scan_history)

            if hasattr(self.home_tab, "update_summary"):
                self.home_tab.update_summary(
                    dependencies,
                    vulnerabilities,
                    scan_history
                )

            print("✅ Dashboard refreshed")

        except Exception as e:
            print(f"❌ Refresh error: {e}")

    # ============================
    # SCAN FUNCTION
    # ============================

    def upload_and_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")

        if not folder:
            return

        project_name = os.path.basename(folder)

        print(f"📁 Scanning: {project_name}")

        self.worker = ScanWorker(project_name, folder)
        self.worker.finished.connect(self.on_scan_complete)
        self.worker.start()

    def on_scan_complete(self):
        print("✅ Scan complete, refreshing UI...")
        self.refresh_data()


# ============================
# RUN APP
# ============================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ style.qss not found")

    window = Dashboard()
    window.show()

    sys.exit(app.exec())