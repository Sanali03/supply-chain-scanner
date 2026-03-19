from PyQt6.QtWidgets import QMainWindow, QTabWidget, QApplication
import sys
from UI_dependencies import DependencyTable
from UI_vulnerabilities import VulnerabilityTable
from UI_reports import ReportViewer
from UI_charts import RiskChart
from UI_scan_history import ScanHistoryTable
from UI_home import HomePage   # import the new file


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supply Chain Scanner Dashboard")
        self.resize(1000, 700)

        tabs = QTabWidget()

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
        tabs.addTab(DependencyTable(dependencies), "Dependencies")
        tabs.addTab(VulnerabilityTable(vulnerabilities), "Vulnerabilities")
        tabs.addTab(RiskChart(dependencies), "Risk Chart")
        tabs.addTab(ReportViewer(), "Reports")
        tabs.addTab(ScanHistoryTable(scan_history), "Scan History")

        self.setCentralWidget(tabs)


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
