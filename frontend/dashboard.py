from PyQt6.QtWidgets import QMainWindow, QTabWidget, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
from UI_dependencies import DependencyTable
from UI_vulnerabilities import VulnerabilityTable
from UI_reports import ReportViewer
from UI_charts import RiskChart
from UI_scan_history import ScanHistoryTable
from UI_home import HomePage


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supply Chain Scanner Dashboard")
        self.resize(1400, 800)

        # ==================== MAIN CONTAINER ====================
        main_container = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==================== LEFT SIDEBAR ====================
        sidebar = QWidget()
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #1a1f3a;
                border-right: 1px solid #3d4661;
            }
        """)
        sidebar.setMaximumWidth(200)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)

        # Logo/Title
        logo = QLabel("Supply Chain\nScanner")
        logo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        logo.setStyleSheet("color: #3498db; padding: 10px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo)

        # Separator
        separator = QLabel("—" * 15)
        separator.setStyleSheet("color: #3d4661; padding: 5px;")
        sidebar_layout.addWidget(separator)

        # Navigation buttons
        nav_buttons = [
            ("Home", 0),
            ("Dependencies", 1),
            ("Vulnerabilities", 2),
            ("Risk Chart", 3),
            ("Reports", 4),
            ("Scan History", 5),
        ]

        self.nav_buttons = {}
        for btn_text, tab_index in nav_buttons:
            btn = QPushButton(btn_text)
            btn.setFont(QFont("Arial", 10))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #bdc3c7;
                    padding: 12px 15px;
                    border: none;
                    text-align: left;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #2d3561;
                    color: #3498db;
                }
                QPushButton:pressed {
                    background-color: #3498db;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda checked, idx=tab_index: self.switch_tab(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[tab_index] = btn

        sidebar_layout.addStretch()

        # Settings/Help at bottom
        settings_btn = QPushButton("Settings")
        settings_btn.setFont(QFont("Arial", 10))
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #95a5a6;
                padding: 12px 15px;
                border: none;
                text-align: left;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2d3561;
                color: #3498db;
            }
        """)
        sidebar_layout.addWidget(settings_btn)

        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)

        # ==================== RIGHT CONTENT AREA ====================
        content = QWidget()
        content.setStyleSheet("background-color: #1a1f3a;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #2d3561;
                color: #bdc3c7;
                padding: 8px 20px;
                border: 1px solid #3d4661;
                border-radius: 0px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
                border: none;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3d4661;
            }
        """)

        # Dummy data for now (later load from DB)
        dependencies = [
            {"name": "flask", "version": "2.2.5", "risk": "Low", "vendor": "PyPI"},
            {"name": "requests", "version": "2.31.0", "risk": "Medium", "vendor": "PyPI"},
            {"name": "django", "version": "5.0.1", "risk": "High", "vendor": "PyPI"},
        ]
        vulnerabilities = [
            {"cve": "CVE-2024-12345", "severity": "High", "package": "requests"},
        ]
        scan_history = [
            {"date": "2026-03-01", "file": "sbom1.json", "deps": 12, "vulns": 3},
            {"date": "2026-03-03", "file": "sbom2.json", "deps": 8, "vulns": 1},
        ]

        # Add tabs
        self.tabs.addTab(HomePage(), "Home")
        self.tabs.addTab(DependencyTable(dependencies), "Dependencies")
        self.tabs.addTab(VulnerabilityTable(vulnerabilities), "Vulnerabilities")
        self.tabs.addTab(RiskChart(dependencies), "Risk Chart")
        self.tabs.addTab(ReportViewer(), "Reports")
        self.tabs.addTab(ScanHistoryTable(scan_history), "Scan History")

        # Hide tab bar (we'll use sidebar for navigation)
        self.tabs.tabBar().hide()

        content_layout.addWidget(self.tabs)
        content.setLayout(content_layout)
        main_layout.addWidget(content)

        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        # Set home as default tab
        self.tabs.setCurrentIndex(0)

    def switch_tab(self, index):
        """Switch to a specific tab"""
        self.tabs.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load stylesheet AFTER app is created
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠️ style.qss not found, running without custom styles.")

    window = Dashboard()
    window.show()
    sys.exit(app.exec())
