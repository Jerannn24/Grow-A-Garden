import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QPushButton
from PyQt5.QtCore import Qt, QDateTime
from models.UserModel import DB_FILE_PATH

class SharePostWidget(QWidget):
    def __init__(self, post_manager, parent=None):
        super().__init__(parent)
        self.post_manager = post_manager
        
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: none;
            padding: 10px;
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(frame)

        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(15, 15, 15, 15)
        frame_layout.setSpacing(12)
        
        avatar_lbl = QLabel("🌱")
        avatar_lbl.setFixedSize(40, 40)
        avatar_lbl.setAlignment(Qt.AlignCenter)
        avatar_lbl.setStyleSheet("""
            background-color: #E8F5E9; 
            border-radius: 20px; 
            font-size: 18px;
        """)
        
        # Placeholder Buat Post 
        self.input_label = QLabel("Share your gardening moment...")
        self.input_label.setCursor(Qt.PointingHandCursor)
        self.input_label.setStyleSheet("font-size: 15px; color: gray; padding: 8px 12px; background-color: #F5F5F5; border-radius: 20px; border: none;")

        self.post_button = QPushButton("Add Post")
        self.post_button.setFixedSize(110, 35)
        self.post_button.setStyleSheet("""
            QPushButton {
                background-color: #66BB6A;
                color: white; 
                border-radius: 17px; 
                font-weight: bold;
                font-size: 13px;
                border : none;
                padding : 5px 15px;
            }
            QPushButton:hover {
                background-color: #57A05A;
            }
        """)
        self.post_button.clicked.connect(self._open_create_post)

        frame_layout.addWidget(avatar_lbl)
        frame_layout.addWidget(self.input_label)
        frame_layout.addStretch()
        frame_layout.addWidget(self.post_button)

        self.input_label.mousePressEvent = lambda event: self._open_create_post()

    def _open_create_post(self):
        if hasattr(self.post_manager, 'switch_to_create_post'):
            self.post_manager.switch_to_create_post()