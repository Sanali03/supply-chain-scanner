from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, 
                             QFrame, QGridLayout, QTableWidget, QTableWidgetItem, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1a1f3a;")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # ==================== FILE UPLOAD SECTION ====================
        upload_section = QFrame()
        upload_section.setStyleSheet("""
            QFrame {
                background-color: #2d3561;
                border-radius: 8px;
                border: 2px dashed #3498db;
            }
        """)
        upload_layout = QVBoxLayout()
        
        upload_title = QLabel("Upload File for Analysis")
        upload_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        upload_title.setStyleSheet("color: white;")
        
        upload_subtitle = QLabel("Drag & Drop Files Here or Browse Files")
        upload_subtitle.setFont(QFont("Arial", 11))
        upload_subtitle.setStyleSheet("color: #bdc3c7;")
        upload_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        browse_btn = QPushButton("Browse Files")
        browse_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px 30px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        browse_btn.clicked.connect(self.open_file_dialog)
        
        upload_layout.addWidget(upload_title)
        upload_layout.addWidget(upload_subtitle)
        upload_layout.addWidget(browse_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        upload_section.setLayout(upload_layout)
        upload_section.setMinimumHeight(150)
        
        main_layout.addWidget(upload_section)

        # ==================== STATS SECTION ====================
        stats_layout = QHBoxLayout()
        
        # Risk Assessment
        risk_frame = self.create_stat_frame(" Risk Level", "HIGH", "#e74c3c")
        stats_layout.addWidget(risk_frame)
        
        # Dependencies Count
        deps_frame = self.create_stat_frame(" Dependencies", "56", "#3498db")
        stats_layout.addWidget(deps_frame)
        
        # Vulnerabilities
        vuln_frame = self.create_stat_frame("Vulnerabilities", "28", "#e67e22")
        stats_layout.addWidget(vuln_frame)
        
        # Outdated Libraries
        outdated_frame = self.create_stat_frame("Outdated Libs", "12", "#f39c12")
        stats_layout.addWidget(outdated_frame)
        
        main_layout.addLayout(stats_layout)

        # ==================== RISK ASSESSMENT DETAILS ====================
        details_layout = QHBoxLayout()
        details_layout.setSpacing(15)
        
        # Risk Details Panel
        risk_frame = QFrame()
        risk_frame.setStyleSheet("""
            QFrame {
                background-color: #2d3561;
                border-radius: 8px;
            }
        """)
        risk_layout = QVBoxLayout()
        
        risk_title = QLabel("Risk Assessment Details")
        risk_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        risk_title.setStyleSheet("color: white;")
        
        risk_details = QLabel(
            "Risk Score: 7.5 (High)\n"
            "Critical Dependencies: 5\n"
            "High Severity CVEs: 8\n"
            "Medium Severity CVEs: 12"
        )
        risk_details.setFont(QFont("Arial", 10))
        risk_details.setStyleSheet("color: #ecf0f1;")
        
        risk_layout.addWidget(risk_title)
        risk_layout.addWidget(risk_details)
        risk_layout.addStretch()
        risk_frame.setLayout(risk_layout)
        details_layout.addWidget(risk_frame)
        
        # Recent Scans Panel
        scans_frame = QFrame()
        scans_frame.setStyleSheet("""
            QFrame {
                background-color: #2d3561;
                border-radius: 8px;
            }
        """)
        scans_layout = QVBoxLayout()
        
        scans_title = QLabel("Recent Scans")
        scans_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        scans_title.setStyleSheet("color: white;")
        
        scans_table = QTableWidget()
        scans_table.setColumnCount(3)
        scans_table.setHorizontalHeaderLabels(["Scan ID", "Status", "Time"])
        scans_table.setStyleSheet("""
            QTableWidget {
                background-color: #1a1f3a;
                gridline-color: #3d4661;
                border: none;
            }
            QTableWidget::item {
                color: #ecf0f1;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2d3561;
                color: white;
                padding: 5px;
                border: none;
            }
        """)
        
        # Add sample data
        scans_table.insertRow(0)
        scans_table.setItem(0, 0, QTableWidgetItem("#1052"))
        scans_table.setItem(0, 1, QTableWidgetItem("Completed"))
        scans_table.setItem(0, 2, QTableWidgetItem("10 mins ago"))
        
        scans_table.insertRow(1)
        scans_table.setItem(1, 0, QTableWidgetItem("#1051"))
        scans_table.setItem(1, 1, QTableWidgetItem("High Risk"))
        scans_table.setItem(1, 2, QTableWidgetItem("1 hour ago"))
        
        scans_table.insertRow(2)
        scans_table.setItem(2, 0, QTableWidgetItem("#1050"))
        scans_table.setItem(2, 1, QTableWidgetItem("No Issues"))
        scans_table.setItem(2, 2, QTableWidgetItem("2 hours ago"))
        
        scans_table.setMaximumHeight(120)
        scans_layout.addWidget(scans_title)
        scans_layout.addWidget(scans_table)
        scans_frame.setLayout(scans_layout)
        details_layout.addWidget(scans_frame)
        
        main_layout.addLayout(details_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def create_stat_frame(self, title, value, color):
        """Create a statistics frame with title and value"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: #2d3561;
                border-radius: 8px;
                border-left: 4px solid {color};
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setStyleSheet("color: #bdc3c7;")
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        frame.setLayout(layout)
        return frame

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Select SBOM File", 
            "", 
            "JSON Files (*.json);;CSV Files (*.csv);;XML Files (*.xml);;All Files (*)"
        )
        if file_name:
            print(f"User uploaded file: {file_name}")
            # Later: trigger backend scan here
