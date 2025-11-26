from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QSizePolicy, QMessageBox, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QLocale, pyqtSignal
from models.UserModel import UserModel
from typing import Optional
from datetime import datetime
from models.Plant import Plant
from models.Post import Post
from views.FormChangeProfile import FormChangeProfile

class DisplayProfile(QWidget):
    profileUpdateRequested = pyqtSignal(str, str, str, str)
    def __init__(self, current_user: Optional[UserModel], main_window, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.main_window = main_window
        self.setObjectName("DisplayProfileView")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.plants_value_lbl = None
        self.posts_value_lbl = None

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(30, 20, 30, 0)

        title_lbl = QLabel("<b>My Profile</b>")
        title_lbl.setTextFormat(Qt.RichText)
        title_lbl.setFont(QFont("Arial", 24, QFont.Bold))
        title_lbl.setStyleSheet("color: #2E7D32;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        self.main_layout.addWidget(header_widget)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(50, 0, 50, 0)
        self.content_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.banner_frame = QFrame()
        self.banner_frame.setFixedHeight(180)
        self.banner_frame.setStyleSheet("background-color: #A5D6A7; border-radius: 15px; border: none;")

        self.profile_pic_lbl = QLabel()
        self.profile_pic_lbl.setObjectName('ProfilePic')
        self.profile_pic_lbl.setFixedSize(120, 120)
        self.profile_pic_lbl.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 60px; "
            "border: 5px solid white; font-weight: bold;"
        )
        self.profile_pic_lbl.setFont(QFont("Arial", 36, QFont.Bold))
        self.profile_pic_lbl.setAlignment(Qt.AlignCenter)

        self.edit_btn = QPushButton("✎ Edit Profile")
        self.edit_btn.setStyleSheet(
            "QPushButton { background-color: #66BB6A; color: white; padding: 8px 20px; border-radius: 8px; font-weight: bold; font-size: 11pt; }"
            "QPushButton:hover { background-color: #81C784; }"
            "QPushButton:pressed { background-color: #4CAF50; }"
        )
        self.edit_btn.setFixedSize(160, 40)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.clicked.connect(self.displayEditProfile)

        top_grid = QGridLayout()
        top_grid.setContentsMargins(0, 0, 0, 0)
        top_grid.setSpacing(0)

        top_grid.addWidget(self.banner_frame, 0, 0, 1, 3)

        profile_pic_wrapper = QWidget()
        profile_pic_layout = QVBoxLayout(profile_pic_wrapper)
        profile_pic_layout.setContentsMargins(30, 0, 0, 30)
        profile_pic_layout.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        profile_pic_layout.addWidget(self.profile_pic_lbl)
        top_grid.addWidget(profile_pic_wrapper, 0, 0, 1, 1)

        edit_btn_wrapper = QWidget()
        edit_btn_layout = QVBoxLayout(edit_btn_wrapper)
        edit_btn_layout.setContentsMargins(0, 20, 30, 0)
        edit_btn_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        edit_btn_layout.addWidget(self.edit_btn)
        top_grid.addWidget(edit_btn_wrapper, 0, 2, 1, 1)

        top_grid.setColumnStretch(1, 1)

        self.content_layout.addLayout(top_grid)

        self.name_lbl = QLabel()
        self.name_lbl.setTextFormat(Qt.RichText)
        self.email_lbl = QLabel()
        self.email_lbl.setTextFormat(Qt.RichText)
        self.location_lbl = QLabel()
        self.location_lbl.setTextFormat(Qt.RichText)
        self.info_lbl = QLabel()
        self.info_lbl.setTextFormat(Qt.RichText)
        self.joined_lbl = QLabel()
        self.joined_lbl.setTextFormat(Qt.RichText)

        font_detail = QFont("Arial", 11)
        self.email_lbl.setFont(font_detail)
        self.location_lbl.setFont(font_detail)
        self.joined_lbl.setFont(font_detail)

        data_layout = QVBoxLayout()
        data_layout.setSpacing(8)
        data_layout.setContentsMargins(30, 0, 30, 0)
        data_layout.addSpacing(30)

        data_layout.addWidget(self.name_lbl)
        data_layout.addWidget(self.email_lbl)
        data_layout.addWidget(self.location_lbl)
        data_layout.addSpacing(15)

        stats_widget = QFrame()
        stats_widget.setStyleSheet(
            "QFrame { border: none; background-color: transparent; }" 
        )
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 10, 0, 10) 
        stats_layout.setSpacing(30)

        stats_plants_card = self._create_stat_label("0", "My Plants", "🌱", "plants")
        stats_posts_card = self._create_stat_label("0", "Posts", "💬", "posts")      
        
        # Tambahkan QFrame ke layout
        stats_layout.addWidget(stats_plants_card) 
        stats_layout.addWidget(stats_posts_card)
        
        stats_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed) 
        stats_widget.setMinimumWidth(350)
        stats_widget.setMaximumWidth(450)
        stats_widget.setFixedHeight(110)

        data_layout.addWidget(stats_widget, alignment=Qt.AlignLeft)
        data_layout.addSpacing(20)

        h_separator = QFrame()
        h_separator.setFrameShape(QFrame.HLine)
        h_separator.setFrameShadow(QFrame.Plain) 
        h_separator.setStyleSheet("background-color: #E0E0E0; height: 1px; border: none;") 
        data_layout.addWidget(h_separator)
        data_layout.addSpacing(15)

        self.info_lbl.setStyleSheet("line-height: 1.5;") 
        data_layout.addWidget(self.info_lbl)
        data_layout.addSpacing(15)
        data_layout.addWidget(self.joined_lbl)
        data_layout.addStretch()

        self.content_layout.addLayout(data_layout)

        self.main_layout.addWidget(content_widget)
        self.main_layout.addStretch()

    def _create_stat_label(self, value, description, icon_char, stat_type: str):
        card_frame = QFrame()
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(5)
        card_frame.setFixedSize(160, 90) 

        card_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #C8E6C9;
                border-radius: 12px;
            }
        """)

        value_lbl = QLabel(f"{value}")
        value_lbl.setFont(QFont("Arial", 26, QFont.Bold))
        value_lbl.setStyleSheet("color:#2E7D32;")
        value_lbl.setAlignment(Qt.AlignCenter)
        
        # Simpan referensi QLabel angka ke variabel anggota
        if stat_type == "plants":
            self.plants_value_lbl = value_lbl
        elif stat_type == "posts":
            self.posts_value_lbl = value_lbl

        desc_html = f"<span style='font-size:11px; color:#616161; font-weight: 500;'>{icon_char} {description}</span>"
        desc_lbl = QLabel(desc_html)
        desc_lbl.setTextFormat(Qt.RichText)
        desc_lbl.setAlignment(Qt.AlignCenter)
        
        card_layout.addWidget(value_lbl)
        card_layout.addWidget(desc_lbl)
        
        return card_frame 

    def load_data(self):
        if self.current_user is None:
            self.update_ui_with_data("Guest", "N/A", "N/A", "Please log in to see profile details.", "N/A", 0, 0)
            return

        user = self.current_user
        username = user.getUsername()
        email = user.getEmail()
        location = user.getLocation()
        profile_info = user.getProfileInfo()
        time_created_str = user.getTimeCreated()

        joined_date = "N/A"
        try:
            time_created_obj = datetime.strptime(time_created_str.split(' ')[0], '%Y-%m-%d')
            locale = QLocale(QLocale.English, QLocale.UnitedStates)
            joined_date = locale.toString(time_created_obj, "dd MMMM yyyy")
        except Exception as e:
            print(f"Error parsing date: {e}")
            joined_date = "N/A"

        plant_count = 0
        post_count = 0

        if self.current_user:
            user_id = self.current_user.getUserID()
            plant_count = Plant.countUserPlants(user_id)
            post_count = Post.countUserPosts(user_id)

        self.update_ui_with_data(username, email, location, profile_info, joined_date, plant_count, post_count)

    def update_ui_with_data(self, username, email, location, profile_info, joined_date, current_plant_count, post_count):
        initials = "".join([part[0].upper() for part in username.split() if part][:2]) or "JD"
        self.profile_pic_lbl.setText(initials)

        self.name_lbl.setText(f"<h1 style='font-size:28px; font-weight:bold; margin-top:10px; margin-bottom: 5px; color:#2E7D32;'>{username}</h1>")

        self.email_lbl.setText(f"<span style='color: #4A4A4A; padding: 2px 0; display: block; font-size:11pt;'>📧 <b>Email:</b> {email}</span>")
        self.location_lbl.setText(f"<span style='color: #4A4A4A; padding: 2px 0; display: block; font-size:11pt;'>📍 <b>Location:</b> {location}</span>")

        self.info_lbl.setText(f"<span style='font-weight:bold; font-size:13pt; color:#2E7D32;'>About Me:</span><br/><span style='color: #4A4A4A; font-size:11pt;'>{profile_info or 'No profile information provided.'}</span>")
        self.info_lbl.setWordWrap(True)

        self.joined_lbl.setText(f"<span style='color: #757575; font-size:10pt;'>🗓️ Joined {joined_date}</span>")

        if self.plants_value_lbl:
            self.plants_value_lbl.setText(str(current_plant_count))
        
        if self.posts_value_lbl:
            self.posts_value_lbl.setText(str(post_count))

    def update_user_data(self, new_user: UserModel):
        if new_user is None:
            self.current_user = None
            self.load_data()
            return

        self.current_user = new_user
        self.load_data()

    def displayEditProfile(self):
        if self.current_user is None:
            QMessageBox.warning(self, "Akses Ditolak", "Anda harus login untuk mengedit profil.")
            return
        
        edit_dialog = FormChangeProfile(self.current_user, self)
        edit_dialog.profileUpdateRequested.connect(self.profileUpdateRequested.emit)
        
        if hasattr(self.main_window, 'profileUpdateResponse'):
            self.main_window.profileUpdateResponse.connect(edit_dialog.display_message)
            
        result = edit_dialog.exec_()
        
        if result == QDialog.Accepted:
            self.load_data()