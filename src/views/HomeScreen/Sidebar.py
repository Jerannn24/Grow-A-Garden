from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt


class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(250)
        self._buttons = {}
        
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
        
        layout.addStretch()
        
        self.btn_settings = self.create_nav_btn("⚙️ Settings", "settings")
        layout.addWidget(self.btn_settings)
        
        user_lbl = QLabel("👤 John Doe\nProfile")
        user_lbl.setObjectName('user_info_label')
        user_lbl.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(user_lbl)
        
        self.setLayout(layout)

    def create_nav_btn(self, text, name):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setProperty("class", "nav-btn") 
        self._buttons[name] = btn 
        return btn
    
    def get_nav_buttons(self):
        return self._buttons
