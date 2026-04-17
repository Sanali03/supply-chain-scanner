import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QMovie
from datetime import datetime

# UI Components
from UI_dependencies import DependencyTable
from UI_vulnerabilities import VulnerabilityTable
from UI_reports import ReportViewer
from UI_charts import RiskChart
from UI_scan_history import ScanHistoryTable
from UI_home import HomePage

# Backend
from backend.backend_service import run_scan
from backend.db_service import (
    get_dependencies,
    get_vulnerabilities,
    get_scan_history
)


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

        self.current_project_id = None
        self.project_map = {}

        # ================= MAIN LAYOUT =================
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)

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

        # Upload Button
        scan_btn = QPushButton("📁 Upload Project")
        scan_btn.setObjectName("primaryButton")
        scan_btn.clicked.connect(self.upload_and_scan)
        sidebar_layout.addWidget(scan_btn)

        # Project Dropdown
        self.project_selector = QComboBox()
        self.project_selector.setObjectName("projectSelector")
        self.project_selector.currentTextChanged.connect(self.on_project_change)
        sidebar_layout.addWidget(self.project_selector)

        # ================= NAVIGATION =================
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
            btn.clicked.connect(lambda _, i=idx: self.switch_tab(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # ================= CONTENT =================
        content = QWidget()
        content.setObjectName("content")
        content_layout = QVBoxLayout(content)

        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()

        # Loader
        self.loader = QLabel()
        self.loader.setAlignment(Qt.AlignmentFlag.AlignCenter)

        movie = QMovie("spinner.gif")
        self.loader.setMovie(movie)
        movie.start()
        self.loader.setVisible(False)

        # Tabs
        self.home_tab = HomePage()
        self.dep_tab = DependencyTable([])
        self.vuln_tab = VulnerabilityTable([])
        self.chart_tab = RiskChart([], [])
        self.report_tab = ReportViewer()
        self.history_tab = ScanHistoryTable([])

        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.dep_tab, "Dependencies")
        self.tabs.addTab(self.vuln_tab, "Vulnerabilities")
        self.tabs.addTab(self.chart_tab, "Risk Chart")
        self.tabs.addTab(self.report_tab, "Reports")
        self.tabs.addTab(self.history_tab, "Scan History")

        content_layout.addWidget(self.tabs)
        content_layout.addWidget(self.loader)

        main_layout.addWidget(content)
        self.setCentralWidget(main_container)

        # Load projects AFTER UI ready
        self.load_projects()

        # Default tab
        self.switch_tab(0)

    # ============================
    # LOAD PROJECTS
    # ============================

    def load_projects(self):
        history = get_scan_history()

        self.project_selector.blockSignals(True)
        self.project_selector.clear()
        self.project_map.clear()

        for scan in history:
            dt = datetime.strptime(scan['date'], "%Y-%m-%d %H:%M:%S")
            short_time = dt.strftime("%H:%M")

            label = f"{scan['project']} ({short_time})"

            if label not in self.project_map:  # prevent duplicates
                self.project_selector.addItem(label)
                self.project_map[label] = scan["id"]

        self.project_selector.blockSignals(False)

        if history:
            first = self.project_selector.itemText(0)
            self.current_project_id = self.project_map[first]
            self.project_selector.setCurrentText(first)
            self.refresh_data()

    # ============================
    # PROJECT CHANGE
    # ============================

    def on_project_change(self, text):
        if not text:
            return

        self.current_project_id = self.project_map.get(text)
        self.refresh_data()

    # ============================
    # NAVIGATION
    # ============================

    def switch_tab(self, index):
        self.tabs.setCurrentIndex(index)

        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ============================
    # REFRESH DATA
    # ============================

    def refresh_data(self):
        try:
            if not self.current_project_id:
                return

            dependencies = get_dependencies(self.current_project_id)
            vulnerabilities = get_vulnerabilities(self.current_project_id)
            history = get_scan_history()

            # Get current project name
            current_project_name = self.project_selector.currentText().split(" (")[0]

            # Update UI
            self.dep_tab.update_data(dependencies)
            self.vuln_tab.update_data(vulnerabilities)
            self.chart_tab.update_chart(dependencies, vulnerabilities)
            self.history_tab.update_data(history)

            self.home_tab.update_summary(
                dependencies,
                vulnerabilities,
                history,
                current_project_name
            )

            # ✅ NEW: Update REPORT TAB
            self.report_tab.refresh_report(
                self.current_project_id,
                current_project_name
            )

            print(f"✅ Showing project: {current_project_name}")

        except Exception as e:
            print(f"❌ Refresh error: {e}")

    # ============================
    # SCAN
    # ============================

    def upload_and_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")

        if not folder:
            return

        project_name = os.path.basename(folder)

        self.loader.setVisible(True)
        self.tabs.setVisible(False)

        self.worker = ScanWorker(project_name, folder)
        self.worker.finished.connect(self.on_scan_complete)
        self.worker.start()

    def on_scan_complete(self):
        self.loader.setVisible(False)
        self.tabs.setVisible(True)

        self.load_projects()


# ============================
# RUN APP
# ============================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except:
        print("⚠️ style.qss not found")

    window = Dashboard()
    window.show()

    sys.exit(app.exec())