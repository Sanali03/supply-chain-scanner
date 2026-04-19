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
        self.report_data = {}

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
        self.text_area.setFont(QFont("Segoe UI", 11))

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
    # GENERATE REPORT
    # ============================

    def generate_report(self, project_id=None, project_name=None):
        try:
            self.current_project_id = project_id
            self.current_project_name = project_name

            dependencies = get_dependencies(project_id) if project_id else []
            vulnerabilities = get_vulnerabilities(project_id) if project_id else []
            history = get_scan_history()

            project_history = [h for h in history if h["id"] == project_id] if project_id else history

            dep_count = len(dependencies)
            vuln_count = len(vulnerabilities)
            scan_count = len(project_history)

            latest_scan = project_history[0] if project_history else {}

            # ===== Severity =====
            critical = sum(1 for v in vulnerabilities if v.get("severity", "").upper() == "CRITICAL")
            high = sum(1 for v in vulnerabilities if v.get("severity", "").upper() == "HIGH")
            medium = sum(1 for v in vulnerabilities if v.get("severity", "").upper() == "MEDIUM")
            low = sum(1 for v in vulnerabilities if v.get("severity", "").upper() == "LOW")

            # ===== Risk =====
            overall_risk = latest_scan.get("status", "UNKNOWN")
            risk_score = latest_scan.get("risk_score", 0)

            # ===== Trend =====
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

            # ===== Top Package =====
            package_count = {}
            for v in vulnerabilities:
                pkg = v.get("package", "Unknown")
                package_count[pkg] = package_count.get(pkg, 0) + 1

            top_package = max(package_count, key=package_count.get) if package_count else "N/A"

            # Store data for PDF
            self.report_data = {
                "project": project_name or "ALL PROJECTS",
                "scan_count": scan_count,
                "dep_count": dep_count,
                "vuln_count": vuln_count,
                "latest_date": latest_scan.get("date", "N/A"),
                "latest_risk": latest_scan.get("status", "N/A"),
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low,
                "risk_score": f"{risk_score:.2f}",
                "overall_risk": overall_risk,
                "trend": trend,
                "top_package": top_package
            }

            # ===== BEAUTIFUL HTML =====
            html = f"""
            <h2 style="color:#38bdf8;">SBOM Security Report</h2>

            <h3>Project: <span style="color:#22c55e;">{self.report_data["project"]}</span></h3>
            <hr>

            <h3>Scan Summary</h3>
            <ul>
                <li><b>Total Scans:</b> {scan_count}</li>
                <li><b>Total Dependencies:</b> {dep_count}</li>
                <li><b>Total Vulnerabilities:</b> {vuln_count}</li>
            </ul>

            <h3>Latest Scan</h3>
            <ul>
                <li><b>Date:</b> {self.report_data["latest_date"]}</li>
                <li><b>Risk:</b> {self.report_data["latest_risk"]}</li>
            </ul>

            <h3>Severity Breakdown</h3>
            <ul>
                <li style="color:#ef4444;">CRITICAL: {critical}</li>
                <li style="color:#f97316;">HIGH: {high}</li>
                <li style="color:#f59e0b;">MEDIUM: {medium}</li>
                <li style="color:#22c55e;">LOW: {low}</li>
            </ul>

            <h3>Risk Analysis</h3>
            <ul>
                <li><b>Risk Score:</b> {risk_score:.2f}</li>
                <li><b>Overall Risk:</b> {overall_risk}</li>
                <li><b>Trend:</b> {trend}</li>
            </ul>

            <h3>Key Insights</h3>
            <ul>
                <li>Most vulnerable package: <b>{top_package}</b></li>
                <li>More dependencies → larger attack surface</li>
            </ul>

            <h3>Recommendations</h3>
            <ul>
                <li>Patch CRITICAL & HIGH vulnerabilities immediately</li>
                <li>Keep dependencies updated</li>
                <li>Enable automated scanning</li>
            </ul>
            """

            self.text_area.setHtml(html)

        except Exception as e:
            self.text_area.setText(f"Error generating report:\n{e}")

    # ============================
    # EXPORT PDF (FIXED)
    # ============================

    def export_pdf(self):
        if not self.report_data:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "sbom_report.pdf", "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path)
            styles = getSampleStyleSheet()
            story = []

            d = self.report_data

            story.append(Paragraph("<b>SBOM SECURITY REPORT</b>", styles["Title"]))
            story.append(Spacer(1, 12))

            story.append(Paragraph(f"<b>Project:</b> {d['project']}", styles["Normal"]))
            story.append(Spacer(1, 10))

            story.append(Paragraph("<b>Scan Summary</b>", styles["Heading2"]))
            story.append(Paragraph(f"Total Scans: {d['scan_count']}", styles["Normal"]))
            story.append(Paragraph(f"Dependencies: {d['dep_count']}", styles["Normal"]))
            story.append(Paragraph(f"Vulnerabilities: {d['vuln_count']}", styles["Normal"]))
            story.append(Spacer(1, 10))

            story.append(Paragraph("<b>Latest Scan</b>", styles["Heading2"]))
            story.append(Paragraph(f"Date: {d['latest_date']}", styles["Normal"]))
            story.append(Paragraph(f"Risk: {d['latest_risk']}", styles["Normal"]))
            story.append(Spacer(1, 10))

            story.append(Paragraph("<b>Severity Breakdown</b>", styles["Heading2"]))
            story.append(Paragraph(f"CRITICAL: {d['critical']}", styles["Normal"]))
            story.append(Paragraph(f"HIGH: {d['high']}", styles["Normal"]))
            story.append(Paragraph(f"MEDIUM: {d['medium']}", styles["Normal"]))
            story.append(Paragraph(f"LOW: {d['low']}", styles["Normal"]))
            story.append(Spacer(1, 10))

            story.append(Paragraph("<b>Risk Analysis</b>", styles["Heading2"]))
            story.append(Paragraph(f"Risk Score: {d['risk_score']}", styles["Normal"]))
            story.append(Paragraph(f"Overall Risk: {d['overall_risk']}", styles["Normal"]))
            story.append(Paragraph(f"Trend: {d['trend']}", styles["Normal"]))
            story.append(Spacer(1, 10))

            story.append(Paragraph("<b>Key Insights</b>", styles["Heading2"]))
            story.append(Paragraph(f"Top Package: {d['top_package']}", styles["Normal"]))

            doc.build(story)

        except Exception as e:
            self.text_area.setText(f"PDF Export Error:\n{e}")

    # ============================
    # REFRESH
    # ============================

    def refresh_report(self, project_id=None, project_name=None):
        self.generate_report(project_id, project_name)
