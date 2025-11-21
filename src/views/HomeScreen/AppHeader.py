from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, QDateTime


class AppHeader(QWidget):
    def __init__(self, title_text: str, subtitle_text: str = None):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9FA;")
        
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(5) 

        top_h_layout = QHBoxLayout()
        top_h_layout.setSpacing(20) 
        
        # Time/Date 
        time_col = QVBoxLayout()
        time_col.setContentsMargins(0, 0, 0, 0)
        time_col.setSpacing(2)
        
        date_lbl = QLabel(QDateTime.currentDateTime().toString("dddd, MMMM dd, yyyy"))
        date_lbl.setStyleSheet("color: gray; font-size: 14px;")
        
        time_lbl = QLabel("07:44:14 PM") 
        time_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #007F00;")
        
        time_col.addWidget(date_lbl)
        time_col.addWidget(time_lbl)
        
        top_h_layout.addLayout(time_col)
        top_h_layout.addStretch() 
        
        # Weather Widget 
        weather_frame = QFrame()
        weather_frame.setObjectName("WeatherWidget")
        weather_frame.setFixedSize(120, 40) 
        w_layout = QHBoxLayout(weather_frame)
        w_layout.setContentsMargins(5, 5, 5, 5)
        
        w_icon = QLabel("☀️")
        w_icon.setStyleSheet("font-size: 20px;")
        w_info = QLabel("<b>28°C</b> Sunny")
        w_info.setStyleSheet("font-size: 14px; color: #333;")

        w_layout.addWidget(w_icon)
        w_layout.addWidget(w_info)
        w_layout.addStretch()
        
        top_h_layout.addWidget(weather_frame)
        
        main_v_layout.addLayout(top_h_layout)

        
        title_v_layout = QVBoxLayout()
        title_v_layout.setContentsMargins(0, 5, 0, 0) 
        title_v_layout.setSpacing(2)

        title = QLabel(title_text)
        title.setObjectName("SectionTitle")
        
        if subtitle_text:
            subtitle = QLabel(subtitle_text)
            subtitle.setObjectName("SubTitle")
            title_v_layout.addWidget(title)
            title_v_layout.addWidget(subtitle)
        else:
            title_v_layout.addWidget(title)

        main_v_layout.addLayout(title_v_layout)
