from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QTextEdit, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal
from models.Report import Report


class ReportForm(QWidget):
    reportSubmitted = pyqtSignal(int, str, str)  # postID, violationType, additionalDetails
    
    def __init__(self, post_id: int, parent=None):
        super().__init__(parent)
        self.post_id = post_id
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        header_label = QLabel("📢 Laporkan Post")
        header_label.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #333;
            margin-bottom: 10px;
        """)
        layout.addWidget(header_label)
        
        # Subtitle
        subtitle_label = QLabel("Bantu kami menjaga komunitas tetap aman dan nyaman")
        subtitle_label.setStyleSheet("color: #666; font-size: 13px; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)
        
        # Violation Type
        violation_label = QLabel("Jenis Pelanggaran *")
        violation_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        layout.addWidget(violation_label)
        
        self.violation_combo = QComboBox()
        self.violation_combo.addItems(Report.VIOLATION_TYPES)
        self.violation_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:hover {
                border-color: #007F00;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        layout.addWidget(self.violation_combo)
        
        # Additional Details
        details_label = QLabel("Keterangan Tambahan (Opsional)")
        details_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px; margin-top: 15px;")
        layout.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setPlaceholderText("Jelaskan lebih detail tentang pelanggaran yang terjadi...")
        self.details_text.setMaximumHeight(120)
        self.details_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #007F00;
            }
        """)
        layout.addWidget(self.details_text)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.cancel_btn = QPushButton("Batal")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #666;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        self.cancel_btn.clicked.connect(self.close)
        
        self.submit_btn = QPushButton("Kirim Laporan")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #007F00;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #006600;
            }
        """)
        self.submit_btn.clicked.connect(self._submit_report)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_btn)
        
        layout.addLayout(button_layout)
    
    def _submit_report(self):
        violation_type = self.violation_combo.currentText()
        additional_details = self.details_text.toPlainText().strip()
        
        if not violation_type:
            QMessageBox.warning(self, "Peringatan", "Pilih jenis pelanggaran terlebih dahulu.")
            return
        
        # Emit signal to parent to handle submission
        self.reportSubmitted.emit(self.post_id, violation_type, additional_details)

