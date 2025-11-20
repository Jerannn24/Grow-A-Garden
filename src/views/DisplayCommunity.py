import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QPushButton
from PyQt5.QtCore import Qt, QDateTime
from models.UserModel import DB_FILE_PATH

THIS_FILE = os.path.abspath(__file__)
VIEWS_DIR = os.path.dirname(THIS_FILE)
SRC_DIR = os.path.dirname(VIEWS_DIR)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from controllers.PostManager import PostManager

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


# Share Post
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

# Tampilan Community
class DisplayCommunity(QWidget):
    def __init__(self, db_path: str = DB_FILE_PATH, parent=None):
        super().__init__(parent)
        
        if not os.path.isabs(db_path):
            db_path = os.path.join(SRC_DIR, db_path)
        
        print(f"🌐 DisplayCommunity using database: {db_path}")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30) 
        layout.setSpacing(20)

        header_widget = CommunityHeader()
        layout.addWidget(header_widget) 

        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)

        title_lbl = QLabel("Community Feed")
        title_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-top: 15px;")
        
        title_layout.addWidget(title_lbl)
        
        layout.addWidget(title_container)
        
        # Share Post Widget
        self.post_manager = PostManager(db_path=db_path)
        share_post_widget = SharePostWidget(post_manager=self.post_manager)
        layout.addWidget(share_post_widget)
        
        # Tab Navigation
        tab_layout = QHBoxLayout()
        
        self.btn_recent = self._create_tab_button("Recent", is_active=True)
        self.btn_likes = self._create_tab_button("Top Likes")
        self.btn_views = self._create_tab_button("Top Views")
        
        # Menghubungkan tab ke PostManager
        self.btn_recent.clicked.connect(lambda: self.post_manager.reload_list("timeCreated"))
        self.btn_likes.clicked.connect(lambda: self.post_manager.reload_list("likes"))
        self.btn_views.clicked.connect(lambda: self.post_manager.reload_list("views"))
        
        tab_layout.addWidget(self.btn_recent)
        tab_layout.addWidget(self.btn_likes)
        tab_layout.addWidget(self.btn_views)
        tab_layout.addStretch()
        
        layout.addLayout(tab_layout)

        layout.addWidget(self.post_manager)
        
        layout.addStretch()
        
    def _create_tab_button(self, text, is_active=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setChecked(is_active)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #EFEFEF; 
                border: 1px solid #DDD; 
                border-radius: 15px; 
                padding: 5px 15px;
                margin-right: 5px;
            }
            QPushButton:checked {
                background-color: #007F00;
                color: white; 
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
            QPushButton:checked:hover {
                background-color: #006600;
            }
        """)
        return btn