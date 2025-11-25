from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class RemovePlantForm(QDialog):
    def __init__(self, plant_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Plant")
        self.setFixedSize(350, 200)
        self.setModal(True)
        
        self.setStyleSheet("""
            QDialog { background-color: white; border-radius: 10px; }
            QLabel { color: #333; }
            QPushButton { border-radius: 6px; font-weight: bold; padding: 8px; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        lbl_icon = QLabel("🗑️")
        lbl_icon.setAlignment(Qt.AlignCenter)
        lbl_icon.setFont(QFont("Arial", 30))
        layout.addWidget(lbl_icon)

        lbl_title = QLabel("Delete Plant?")
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(lbl_title)

        lbl_msg = QLabel(f"Are you sure you want to remove '{plant_name}'?\nThis action cannot be undone.")
        lbl_msg.setAlignment(Qt.AlignCenter)
        lbl_msg.setWordWrap(True)
        lbl_msg.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(lbl_msg)

        btn_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setStyleSheet("background-color: #f0f0f0; color: #333; border: none;")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.setStyleSheet("background-color: #dc3545; color: white; border: none;")
        self.btn_delete.clicked.connect(self.accept)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_delete)
        
        layout.addLayout(btn_layout)