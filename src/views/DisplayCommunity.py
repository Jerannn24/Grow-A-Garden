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
from .Community import CommunityHeader, SharePostWidget

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