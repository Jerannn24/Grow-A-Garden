from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from models.UserModel import UserModel
from typing import Optional
from datetime import datetime
from models.Plant import Plant
class DisplayProfile(QWidget):
    def __init__(self, current_user: Optional[UserModel], main_window, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.main_window = main_window
        self.setObjectName("DisplayProfileView")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(30, 20, 30, 0)
        
        # Mengganti **My Profile** dengan <b>My Profile</b>
        title_lbl = QLabel("← <b>My Profile</b>")
        title_lbl.setTextFormat(Qt.RichText)
        title_lbl.setFont(QFont("Arial", 20, QFont.Bold))
        
        header_layout.addWidget(title_lbl) 
        header_layout.addStretch()
        self.main_layout.addWidget(header_widget)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(50, 0, 50, 0)
        self.content_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.banner_frame = QFrame()
        self.banner_frame.setFixedHeight(150)
        self.banner_frame.setStyleSheet("background-color: #E8F5E9; border-radius: 10px; border: 1px solid #C8E6C9;")
        
        self.profile_pic_lbl = QLabel()
        self.profile_pic_lbl.setObjectName('ProfilePic')
        self.profile_pic_lbl.setStyleSheet("background-color: #007F00; color: white; border-radius: 50px; min-width: 100px; max-width: 100px; min-height: 100px; max-height: 100px; border: 4px solid white;")
        self.profile_pic_lbl.setFont(QFont("Arial", 28, QFont.Bold))
        self.profile_pic_lbl.setAlignment(Qt.AlignCenter)
        
        self.edit_btn = QPushButton("✎ Edit Profile")
        self.edit_btn.setStyleSheet("background-color: #007F00; color: white; padding: 5px 15px; border-radius: 5px; font-weight: bold;")
        self.edit_btn.setFixedSize(130, 35)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        
        self.edit_btn.clicked.connect(self.displayEditProfile) 
        
        top_grid = QGridLayout()
        top_grid.addWidget(self.profile_pic_lbl, 0, 0, 2, 1, Qt.AlignLeft | Qt.AlignTop)
        top_grid.addWidget(self.edit_btn, 1, 1, 1, 1, Qt.AlignRight | Qt.AlignBottom)
        top_grid.setColumnStretch(1, 1)
        top_grid.setContentsMargins(30, -70, 30, 0)
        
        self.name_lbl = QLabel()
        self.name_lbl.setTextFormat(Qt.RichText)
        self.email_lbl = QLabel()
        self.email_lbl.setTextFormat(Qt.RichText)
        self.location_lbl = QLabel()
        self.location_lbl.setTextFormat(Qt.RichText)
        self.info_lbl = QLabel()
        self.info_lbl.setTextFormat(Qt.RichText)
        self.joined_lbl = QLabel("🗓️ Joined: -")
        self.joined_lbl.setTextFormat(Qt.RichText)
        
        font_detail = QFont("Arial", 11)
        self.email_lbl.setFont(font_detail)
        self.location_lbl.setFont(font_detail)
        self.joined_lbl.setFont(font_detail)
        
        data_layout = QVBoxLayout()
        data_layout.setSpacing(5)
        data_layout.addWidget(self.name_lbl)
        data_layout.addWidget(self.email_lbl)
        data_layout.addWidget(self.location_lbl)
        data_layout.addSpacing(15)
        
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #F0F0F0; border-radius: 8px; padding: 5px; border: none;")
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(10)
        stats_layout.setContentsMargins(15, 10, 15, 10)
        
        # Inisialisasi label statis agar bisa diubah di load_data
        self.stats_plants_lbl = QLabel()
        self.stats_plants_lbl.setTextFormat(Qt.RichText)
        self.stats_plants_lbl.setAlignment(Qt.AlignCenter)
        
        # Label ini akan kita gunakan untuk menampilkan jumlah total tanaman
        self.stats_total_plants_lbl = QLabel()
        self.stats_total_plants_lbl.setTextFormat(Qt.RichText)
        self.stats_total_plants_lbl.setAlignment(Qt.AlignCenter)

        stats_layout.addWidget(self.stats_plants_lbl) # Diganti menjadi self.stats_plants_lbl
        
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #CCCCCC;")
        stats_layout.addWidget(separator)
        
        stats_layout.addWidget(self.stats_total_plants_lbl) # Diganti menjadi self.stats_total_plants_lbl
        
        # Statistik menggunakan CSS inline, tidak ada **
        # stats_plants = QLabel("<div style='font-size:16px; font-weight:bold; color:#007F00;'>12</div><div style='font-size:10px; color:gray;'>Plants</div>")
        # stats_plants.setTextFormat(Qt.RichText)
        # stats_plants.setAlignment(Qt.AlignCenter)
        
        stats_posts = QLabel("<div style='font-size:16px; font-weight:bold; color:#007F00;'>45</div><div style='font-size:10px; color:gray;'>Posts</div>")
        stats_posts.setTextFormat(Qt.RichText)
        stats_posts.setAlignment(Qt.AlignCenter)
        
        # stats_layout.addWidget(stats_plants)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #CCCCCC;")
        stats_layout.addWidget(separator)
        
        stats_layout.addWidget(stats_posts)
        stats_frame.setFixedWidth(250)
        stats_frame.setFixedHeight(60)

        data_layout.addWidget(stats_frame, alignment=Qt.AlignLeft)
        data_layout.addSpacing(20)
        
        h_separator = QFrame()
        h_separator.setFrameShape(QFrame.HLine)
        h_separator.setFrameShadow(QFrame.Sunken)
        h_separator.setStyleSheet("color: #E0E0E0;")
        data_layout.addWidget(h_separator)
        data_layout.addSpacing(10)
        
        data_layout.addWidget(self.info_lbl)
        data_layout.addSpacing(15)
        data_layout.addWidget(self.joined_lbl)
        
        
        self.content_layout.addWidget(self.banner_frame)
        self.content_layout.addLayout(top_grid)
        self.content_layout.addLayout(data_layout)
        
        self.main_layout.addWidget(content_widget)
        self.main_layout.addStretch()


    def load_data(self):
        if self.current_user is None:
            self.update_ui_with_data("Guest", "N/A", "N/A", "Please log in to see profile details.", "N/A", 0)
            return

        user = self.current_user
        username = user.getUsername()
        email = user.getEmail()
        location = user.getLocation()
        profile_info = user.getProfileInfo()
        time_created_str = user.getTimeCreated()
        
        try:
            time_created = datetime.strptime(time_created_str.split()[0], '%Y-%m-%d')
            joined_date = time_created.strftime('%d %B %Y').replace('January', 'Januari') 
        except:
            joined_date = "N/A"
        
        if self.current_user:
            # Panggil metode statis untuk menghitung jumlah tanaman user
            plant_count = Plant.countUserPlants(user.getUserID())
        else:
            plant_count = 0
            
        self.update_ui_with_data(username, email, location, profile_info, joined_date, plant_count)

    def update_ui_with_data(self, username, email, location, profile_info, joined_date, total_plant_count):
        initials = "".join([part[0].upper() for part in username.split() if part]) or "JD"
        self.profile_pic_lbl.setText(initials)
        
        self.name_lbl.setText(f"<h1 style='font-size:24px; font-weight:bold; margin-top:10px; margin-bottom: 5px; color:#004d00;'>{username}</h1>") 
        
        # Mengganti **Email:** dengan <b>Email:</b>
        self.email_lbl.setText(f"<span style='color: #4a4a4a;'>📧 <b>Email:</b> {email}</span>")
        
        # Mengganti **Location:** dengan <b>Location:</b>
        self.location_lbl.setText(f"<span style='color: #4a4a4a;'>📍 <b>Location:</b> {location}</span>")
        
        self.info_lbl.setText(f"<span style='font-weight:bold; font-size:12pt; color:#004d00;'>About Me:</span><br/><span style='color: #4a4a4a;'>{profile_info or 'No profile information provided.'}</span>")
        self.info_lbl.setWordWrap(True)
        self.joined_lbl.setText(f"<span style='color: #757575;'>🗓️ Joined {joined_date}</span>")

        self.stats_total_plants_lbl.setText(
            f"<div style='font-size:16px; font-weight:bold; color:#007F00;'>{total_plant_count}</div>"
            f"<div style='font-size:10px; color:gray;'>Total Plants</div>"
        )

    def update_user_data(self, new_user: UserModel):
        if new_user is None:
            self.current_user = None
            self.load_data()
            return

        self.current_user = new_user
        self.load_data()

    def displayEditProfile(self):
        if hasattr(self.main_window, 'displayEditProfile'):
            self.main_window.displayEditProfile()
        else:
            pass