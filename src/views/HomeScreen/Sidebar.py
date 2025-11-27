from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QByteArray, QSize
from models.UserModel import UserModel
from typing import Optional

ICON_BACKGROUND_STYLE = "border-radius: 50%;"

class Sidebar(QFrame):
    def __init__(self, current_user: Optional[UserModel], parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(250)
        self._buttons = {}
        self.current_user = current_user
        self.is_admin = False
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        
        icon_size = 100
        svg_path = "src/public/icon.svg"
        svg_widget = QSvgWidget()
        icon_to_add = None
        
        try:
            with open(svg_path, 'rb') as f:
                svg_data = f.read()
            svg_widget.load(QByteArray(svg_data))
        except FileNotFoundError:
            svg_widget = None

        if svg_widget and svg_widget.renderer().isValid():
            svg_widget.setFixedSize(icon_size , icon_size)
            icon_frame = QFrame()
            icon_frame.setFixedSize(icon_size, icon_size)
            icon_frame.setStyleSheet("""
                background-color: #A5D6A7;
                border-radius: 50%;
            """)

            frame_layout = QVBoxLayout(icon_frame)
            frame_layout.setContentsMargins(0, 0, 0, 0)
            frame_layout.addWidget(svg_widget, alignment=Qt.AlignCenter)

            icon_to_add = icon_frame
        else:
            fallback_label = QLabel("🌱") 
            fallback_label.setStyleSheet("font-size: 40px; color: green; padding: 20px; {ICON_BACKGROUND_STYLE} margin-bottom: 5px;")
            fallback_label.setFixedSize(icon_size + 20, icon_size + 20)
            fallback_label.setAlignment(Qt.AlignCenter)
            icon_to_add = fallback_label
            
        layout.addWidget(icon_to_add, alignment=Qt.AlignCenter)
        
        title = QLabel("Grow a Garden")
        title.setObjectName("AppTitle")
        title.setStyleSheet("""
            QLabel#AppTitle {
                color: white; 
                font-size: 22px; 
                font-weight: bold; 
            }
        """)
        layout.addWidget(title)
        layout.addSpacing(20)

        self.btn_home = self.create_nav_btn("🏠 Home", "home")
        self.btn_comm = self.create_nav_btn("👥 Community", "community")
        self.btn_todo = self.create_nav_btn("✅ Todo List", "todo")
        
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_comm)
        layout.addWidget(self.btn_todo)
        
        layout.addStretch()
        
        self.btn_settings = self.create_nav_btn("⚙️ Settings", "settings")
        layout.addWidget(self.btn_settings)
        
        if self.current_user is not None:
            username = self.current_user.getUsername()
            initials = "".join([part[0].upper() for part in username.split() if part]) or "JD"
        else:
            username = "Guest User"
            initials = "G"
        
        initials = "".join([part[0].upper() for part in username.split() if part]) or "JD"
        button_text = f"  {initials}  {username}\n  Profile"
        
        self.btn_profile_final = QPushButton(button_text)
        self.btn_profile_final.setObjectName("profile_button")
        self.btn_profile_final.setProperty("class", "nav-btn-profile")
        self.btn_profile_final.setStyleSheet("""
            QPushButton#profile_button {
                background-color: transparent; 
                color: white; 
                text-align: left;
                padding: 10px;
                border: none;
                line-height: 1.2;
            }
            QPushButton#profile_button:hover {
                background-color: rgba(255, 255, 255, 0.1); 
            }
        """)
        
        self._buttons['profile'] = self.btn_profile_final
        layout.addWidget(self.btn_profile_final)
        
        # user_lbl = QLabel("👤 John Doe\nProfile")
        # user_lbl.setObjectName('user_info_label')
        # user_lbl.setStyleSheet("color: white; padding: 10px;")
        # layout.addWidget(user_lbl)
        
        self.setLayout(layout)

    def create_nav_btn(self, text, name):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setProperty("class", "nav-btn") 
        self._buttons[name] = btn 
        return btn
    
    def create_nav_btn_profile(self, text, name):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setProperty("class", "nav-btn") 
        self._buttons[name] = btn 
        return btn
    
    def connect_profile_action(self, slot_function):
        self.btn_profile_final.clicked.connect(slot_function)
    
    def update_profile_button(self, user_model: UserModel):
        self.current_user = user_model
        username = self.current_user.getUsername()
        initials = "".join([part[0].upper() for part in username.split() if part]) or "JD"
        button_text = f"  {initials}  {username}\n  Profile"
        self.btn_profile_final.setText(button_text)
        
    def get_nav_buttons(self):
        return self._buttons
