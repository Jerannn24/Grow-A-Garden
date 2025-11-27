from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QFrame, QMessageBox, QDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from models.Report import Report
from models.UserModel import UserModel


class AdminActionForm(QWidget):
    actionSubmitted = pyqtSignal(int, str)  # reportID, action
    
    def __init__(self, report_id: int, post_id: int, reporter_name: str, violation_type: str, parent=None):
        super().__init__(parent)
        self.report_id = report_id
        self.post_id = post_id
        self._init_ui(reporter_name, violation_type)
    
    def _init_ui(self, reporter_name: str, violation_type: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        header_label = QLabel("⚡ Tindakan Admin")
        header_label.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #333;
            margin-bottom: 10px;
        """)
        layout.addWidget(header_label)
        
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(8)
        
        info_label = QLabel("Informasi Laporan:")
        info_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        info_layout.addWidget(info_label)
        
        reporter_lbl = QLabel(f"Pelapor: {reporter_name}")
        reporter_lbl.setStyleSheet("color: #666; font-size: 13px;")
        info_layout.addWidget(reporter_lbl)
        
        violation_lbl = QLabel(f"Jenis Pelanggaran: {violation_type}")
        violation_lbl.setStyleSheet("color: #666; font-size: 13px;")
        info_layout.addWidget(violation_lbl)
        
        layout.addWidget(info_frame)
        
        action_label = QLabel("Pilih Tindakan *")
        action_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px; margin-top: 10px;")
        layout.addWidget(action_label)
        
        self.action_combo = QComboBox()
        self.action_combo.addItems(Report.ADMIN_ACTIONS)
        self.action_combo.setStyleSheet("""
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
        layout.addWidget(self.action_combo)
        
        layout.addStretch()
        
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
        
        self.submit_btn = QPushButton("Terapkan Tindakan")
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
        self.submit_btn.clicked.connect(self._submit_action)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_btn)
        
        layout.addLayout(button_layout)
    
    def _submit_action(self):
        action = self.action_combo.currentText()
        
        if not action:
            QMessageBox.warning(self, "Peringatan", "Pilih tindakan terlebih dahulu.")
            return

        confirm_msg = f"Apakah Anda yakin ingin {action.lower()}?"
        reply = QMessageBox.question(self, "Konfirmasi", confirm_msg, 
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.actionSubmitted.emit(self.report_id, action)
            QMessageBox.information(self, "Berhasil", "Tindakan telah diterapkan.")
            self.close()

