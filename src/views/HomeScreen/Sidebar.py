from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from models.UserModel import UserModel
from typing import Optional
class Sidebar(QFrame):
    def __init__(self, current_user: Optional[UserModel], parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(250)
        self._buttons = {}
        self.is_admin = False
        self.current_user = current_user
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        
        title = QLabel("Grow a Garden")
        title.setObjectName("AppTitle")
        layout.addWidget(title)
        layout.addSpacing(20)

        self.btn_home = self.create_nav_btn("🏠 Home", "home")
        self.btn_comm = self.create_nav_btn("👥 Community", "community")
        self.btn_todo = self.create_nav_btn("✅ Todo List", "todo")
        
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_comm)
        layout.addWidget(self.btn_todo)
        
        self.btn_reports = self.create_nav_btn("📋 Reports", "reports")
        self.btn_reports.hide()
        layout.addWidget(self.btn_reports)
        
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
    
    def set_admin_mode(self, is_admin: bool):
        """Menampilkan/menyembunyikan tombol admin report berdasarkan role."""
        self.is_admin = is_admin
        if is_admin:
            self.btn_reports.show()
        else:
            self.btn_reports.hide()

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
