import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QPushButton
from PyQt5.QtCore import Qt, QDateTime
from models.UserModel import DB_FILE_PATH

class CommunityHeader(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9FA;")
        
        main_h_layout = QHBoxLayout(self)
        main_h_layout.setContentsMargins(0, 0, 0, 0) 
        main_h_layout.setSpacing(10)

        # TIME COLUMN
        time_col = QVBoxLayout()
        time_col.setContentsMargins(0, 0, 0, 0)
        time_col.setSpacing(2)

        current_datetime = QDateTime.currentDateTime()
        date_lbl = QLabel(current_datetime.toString("dddd, MMMM dd, yyyy"))
        date_lbl.setStyleSheet("color: gray; font-size: 14px;")
        
        time_lbl = QLabel(current_datetime.toString("hh:mm:ss AP"))
        time_lbl.setStyleSheet("font-size: 30px; font-weight: bold; color: #007F00;")
        
        time_col.addWidget(date_lbl)
        time_col.addWidget(time_lbl)

        main_h_layout.addLayout(time_col)
        main_h_layout.addStretch()

        # INFO
        def create_info_box(icon, main_text, sub_text=None, location=None):
            frame = QFrame()
            frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 5px 10px; border: 1px solid #ddd;")
            v_layout = QVBoxLayout(frame)
            v_layout.setContentsMargins(5, 5, 5, 5)
            v_layout.setSpacing(2)
            
            h_top_layout = QHBoxLayout()
            h_top_layout.setContentsMargins(0, 0, 0, 0)
            
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet("font-size: 16px;")
            
            main_lbl = QLabel(f"<b>{main_text}</b>")
            main_lbl.setStyleSheet("font-size: 14px; margin-left: 5px;")
            
            h_top_layout.addWidget(icon_lbl)
            h_top_layout.addWidget(main_lbl)
            h_top_layout.addStretch()
            
            v_layout.addLayout(h_top_layout)

            if sub_text:
                sub_lbl = QLabel(sub_text)
                sub_lbl.setStyleSheet("color: gray; font-size: 11px; margin-left: 18px;")
                v_layout.addWidget(sub_lbl)
            
            if location:
                loc_lbl = QLabel(location)
                loc_lbl.setStyleSheet("color: #795548; font-size: 11px; margin-left: 18px;")
                v_layout.addWidget(loc_lbl)

            return frame

        main_h_layout.addWidget(create_info_box("☀️", "28°C", "Sunny"))
        main_h_layout.addWidget(create_info_box("💨", "12 km/h", "Humidity: 65%"))
        main_h_layout.addWidget(create_info_box("📍", "Jakarta, Indonesia"))