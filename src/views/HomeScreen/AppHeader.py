from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, QDateTime, QTimer


class AppHeader(QWidget):
    def __init__(self, title_text: str, subtitle_text: str = None):
        super().__init__()
        
        self.setStyleSheet("""
            AppHeader {
                background-color: white;
                border-bottom: 1px solid #E0E0E0;
            }
        """)
        
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(30, 20, 30, 20)
        main_v_layout.setSpacing(10) 

        top_h_layout = QHBoxLayout()
        top_h_layout.setSpacing(20) 
        
        # Time/Date 
        time_col = QVBoxLayout()
        time_col.setContentsMargins(0, 0, 0, 0)
        time_col.setSpacing(2)
        
        self.date_lbl = QLabel()
        self.date_lbl.setStyleSheet("color: gray; font-size: 13px; border: none;")
        
        self.time_lbl = QLabel() 
        self.time_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #007F00; border: none;")
        
        time_col.addWidget(self.date_lbl)
        time_col.addWidget(self.time_lbl)
        
        top_h_layout.addLayout(time_col)
        top_h_layout.addStretch() 
        
        # Weather Widget 
        weather_frame = QFrame()
        weather_frame.setObjectName("WeatherWidget")
        weather_frame.setFixedSize(140, 50) 
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
        title_v_layout.setContentsMargins(0, 10, 0, 0) 
        title_v_layout.setSpacing(5)

        self.title_lbl = QLabel(title_text)
        self.title_lbl.setObjectName("SectionTitle")
        self.title_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: #333; border: none;")
        
        title_v_layout.addWidget(self.title_lbl)

        if subtitle_text:
            self.subtitle_lbl = QLabel(subtitle_text)
            self.subtitle_lbl.setObjectName("SubTitle")
            self.subtitle_lbl.setStyleSheet("font-size: 14px; color: gray; border: none;")
            title_v_layout.addWidget(self.subtitle_lbl)

        main_v_layout.addLayout(title_v_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        
        self.update_clock()

    def update_clock(self):
        """Fungsi ini dipanggil setiap detik oleh QTimer"""
        current_datetime = QDateTime.currentDateTime()
        
        self.time_lbl.setText(current_datetime.toString("hh:mm:ss AP"))

        self.date_lbl.setText(current_datetime.toString("dddd, MMMM dd, yyyy"))

    def setTitle(self, text):
        self.title_lbl.setText(text)

    def setSubtitle(self, text):
        if hasattr(self, 'subtitle_lbl'):
            self.subtitle_lbl.setText(text)
