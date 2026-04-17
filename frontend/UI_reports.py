from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton, QFileDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Backend
from backend.db_service import get_dependencies, get_vulnerabilities, get_scan_history

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class ReportViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.current_project_id = None
        self.current_project_name = None

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ===== Title =====
        title = QLabel("Reports & Insights")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # ===== Export Button =====
        self.export_btn = QPushButton("Export Report to PDF")
        self.export_btn.setObjectName("primaryButton")
        self.export_btn.clicked.connect(self.export_pdf)
        layout.addWidget(self.export_btn)

        # ===== Report Area =====
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont("Consolas", 11))

        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #1f2937;
                color: #e5e7eb;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.08);
            }
        """)

        layout.addWidget(self.text_area)

        self.setLayout(layout)

    # ============================
    # GENERATE REPORT (FIXED)
    # ============================

    def generate_report(self, project_id=None, project_name=None):
        try:
            self.current_project_id = project_id
            self.current_project_name = project_name

            # ✅ CORRECT DATA FETCHING
            dependencies = get_dependencies(project_id) if project_id else []
            vulnerabilities = get_vulnerabilities(project_id) if project_id else []
            history = get_scan_history()

            project_history = [
                h for h in history if h["id"] == project_id
            ] if project_id else history

            dep_count = len(dependencies)
            vuln_count = len(vulnerabilities)
            scan_count = len(project_history)

            latest_scan = project_history[0] if project_history else {}

            # ===== SEVERITY =====
            critical = sum(1 for v in vulnerabilities if v.get("severity", "").upper() == "CRITICAL")
            high = sum(1 for v in vulnerabilities if v.get("severity", "").upper() == "HIGH")
            medium = sum(1 for v in vulnerabilities if v.get("severity", "").upper() == "MEDIUM")
            low = sum(1 for v in vulnerabilities if v.get("severity", "").upper() == "LOW")

            # ===== RISK =====
            risk_score = (critical * 3 + high * 2 + medium) / max(1, vuln_count)

            if risk_score >= 2:
                overall_risk = "HIGH"
            elif risk_score >= 1:
                overall_risk = "MEDIUM"
            else:
                overall_risk = "LOW"

            # ===== TREND =====
            trend = "N/A"
            if len(project_history) >= 2:
                latest = project_history[0].get("vulns", 0)
                previous = project_history[1].get("vulns", 0)

                if latest > previous:
                    trend = "INCREASING ⚠️"
                elif latest < previous:
                    trend = "DECREASING ✅"
                else:
                    trend = "STABLE"

            # ===== TOP PACKAGE =====
            package_count = {}
            for v in vulnerabilities:
                pkg = v.get("package", "Unknown")
                package_count[pkg] = package_count.get(pkg, 0) + 1

            top_package = max(package_count, key=package_count.get) if package_count else "N/A"

            # ===== REPORT TEXT =====
            self.report_text = f"""
SBOM SECURITY REPORT
====================

Project: {project_name}

Scan Summary
------------
Total Scans          : {scan_count}
Total Dependencies   : {dep_count}
Total Vulnerabilities: {vuln_count}

Latest Scan
------------
Date : {latest_scan.get("date", "N/A")}
Risk : {latest_scan.get("status", "N/A")}

Severity Breakdown
------------------
CRITICAL : {critical}
HIGH     : {high}
MEDIUM   : {medium}
LOW      : {low}

Risk Analysis
-------------
Risk Score   : {risk_score:.2f}
Overall Risk : {overall_risk}
Trend        : {trend}

Key Insights
------------
- Most vulnerable package: {top_package}
- Larger dependency trees increase risk exposure
- Critical vulnerabilities must be patched immediately

Recommendations
---------------
- Patch CRITICAL & HIGH vulnerabilities immediately
- Keep dependencies updated
- Use dependency pinning
- Automate security scans
- Integrate SBOM in CI/CD
"""

            self.text_area.setText(self.report_text)

        except Exception as e:
            self.text_area.setText(f"Error generating report:\n{e}")

    # ============================
    # EXPORT PDF
    # ============================

    def export_pdf(self):
        if not hasattr(self, "report_text"):
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            "sbom_report.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path)
            styles = getSampleStyleSheet()

            story = []

            for line in self.report_text.split("\n"):
                story.append(Paragraph(line, styles["Normal"]))
                story.append(Spacer(1, 8))

            doc.build(story)

        except Exception as e:
            self.text_area.setText(f"PDF Export Error:\n{e}")

    # ============================
    # REFRESH FROM DASHBOARD
    # ============================

    def refresh_report(self, project_id=None, project_name=None):
        self.generate_report(project_id, project_name)
