import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QComboBox, QMessageBox   # ✅ NEW
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
    get_scan_history,
    get_project_path,
    delete_project   
) 
from backend.init_db import create_tables
# ============================
# THREAD WORKER
# ============================

class ScanWorker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, project_name, project_path):
        super().__init__()
        self.project_name = project_name
        self.project_path = project_path

    def run(self):
        try:
            run_scan(
                self.project_name,
                self.project_path,
                progress_callback=self.progress.emit
            )
        except Exception as e:
            print(f" Scan error: {e}")
        self.finished.emit()


# ============================
# DASHBOARD
# ============================

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize database and migrations
        create_tables()
        
        self.setWindowTitle("Supply Chain Scanner Dashboard")
        self.resize(1400, 800)

        self.current_project_id = None
        self.project_map = {}

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

        logo = QLabel("Supply Chain\nScanner")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        sidebar_layout.addWidget(logo)

        scan_btn = QPushButton("Upload Project")
        scan_btn.setObjectName("primaryButton")
        scan_btn.clicked.connect(self.upload_and_scan)
        sidebar_layout.addWidget(scan_btn)

        # RESCAN BUTTON
        rescan_btn = QPushButton(" Re-Scan Project")
        rescan_btn.setObjectName("primaryButton")
        rescan_btn.clicked.connect(self.rescan_project)
        sidebar_layout.addWidget(rescan_btn)

        self.project_selector = QComboBox()
        self.project_selector.setObjectName("projectSelector")
        self.project_selector.currentTextChanged.connect(self.on_project_change)
        sidebar_layout.addWidget(self.project_selector)

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

        # DELETE BUTTON (BOTTOM)
        delete_btn = QPushButton("🗑 Delete Project")
        delete_btn.setObjectName("primaryButton")
        delete_btn.clicked.connect(self.delete_selected_project)
        sidebar_layout.addWidget(delete_btn)

        main_layout.addWidget(sidebar)

        # ================= CONTENT =================
        content = QWidget()
        content.setObjectName("content")
        content_layout = QVBoxLayout(content)

        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()

        # ================= LOADER =================
        self.loader = QLabel()
        self.loader.setAlignment(Qt.AlignmentFlag.AlignCenter)

        spinner_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "spinner.gif")
        )

        self.movie = QMovie(spinner_path)

        if not self.movie.isValid():
            print(" Spinner GIF not found or invalid")

        self.loader.setMovie(self.movie)
        self.loader.setFixedSize(100, 100)
        self.loader.setScaledContents(True)

        self.progress_label = QLabel("Scanning... 0%")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("color: white; font-size: 16px;")

        # CENTERED LOADER
        self.loader_container = QWidget()
        loader_layout = QVBoxLayout(self.loader_container)
        loader_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loader_layout.setSpacing(10)

        loader_layout.addWidget(self.loader)
        loader_layout.addWidget(self.progress_label)

        self.loader_container.hide()

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
        content_layout.addWidget(self.loader_container)

        main_layout.addWidget(content)
        self.setCentralWidget(main_container)

        self.load_projects()
        self.switch_tab(0)

    # ============================
    # DELETE PROJECT
    # ============================

    def delete_selected_project(self):
        if not self.current_project_id:
            print(" No project selected")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this project?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            delete_project(self.current_project_id)
            self.load_projects()
            print(" Project deleted")

    # ============================

    def rescan_project(self):
        if not self.current_project_id:
            print("No project selected for rescan")
            return

        project_path = get_project_path(self.current_project_id)

        if not project_path or not os.path.exists(project_path):
            print(" Project path not found")
            return

        project_name = self.project_selector.currentText().split(" (")[0]

        self.tabs.hide()
        self.loader_container.show()
        self.movie.start()
        self.progress_label.setText("Re-scanning... 0%")

        QApplication.processEvents()

        self.worker = ScanWorker(project_name, project_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_scan_complete)
        self.worker.start()

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

            if label not in self.project_map:
                self.project_selector.addItem(label)
                self.project_map[label] = scan["id"]

        self.project_selector.blockSignals(False)

        if history:
            first = self.project_selector.itemText(0)
            self.current_project_id = self.project_map[first]
            self.project_selector.setCurrentText(first)
            self.refresh_data()

    def on_project_change(self, text):
        if not text:
            return
        self.current_project_id = self.project_map.get(text)
        self.refresh_data()

    def switch_tab(self, index):
        self.tabs.setCurrentIndex(index)

        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def refresh_data(self):
        try:
            if not self.current_project_id:
                return

            dependencies = get_dependencies(self.current_project_id)
            vulnerabilities = get_vulnerabilities(self.current_project_id)
            history = get_scan_history()

            current_project_name = self.project_selector.currentText().split(" (")[0]

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

            self.home_tab.trend_chart.update_chart(history)

            self.report_tab.refresh_report(
                self.current_project_id,
                current_project_name
            )


        except Exception as e:
            print(f" Refresh error: {e}")

    # ============================

    def upload_and_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")

        if not folder:
            return

        project_name = os.path.basename(folder)

        self.tabs.hide()
        self.loader_container.show()
        self.movie.start()
        self.progress_label.setText("Scanning... 0%")

        QApplication.processEvents()

        self.worker = ScanWorker(project_name, folder)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_scan_complete)
        self.worker.start()

    def update_progress(self, value):
        self.progress_label.setText(f"Scanning... {value}%")

    def on_scan_complete(self):
        self.movie.stop()
        self.loader_container.hide()
        self.tabs.show()
        self.load_projects()


# ============================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except:
        print(" style.qss not found")

    window = Dashboard()
    window.show()

    sys.exit(app.exec())