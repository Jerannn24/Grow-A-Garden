from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCheckBox, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor
from views.ChangePasswordPopUp import ChangePasswordPopUp


class DisplaySettings(QWidget):
    """Settings page for user preferences and account management"""
    
    # Signals
    password_changed = pyqtSignal(str, str)  # Emits (new_password, confirm_password)
    settings_changed = pyqtSignal(dict)  # Emits dict with changed settings
    logoutRequested = pyqtSignal()
    
    def __init__(self, parent=None, user_model=None):
        super().__init__(parent)
        self.password_popup = None
        self.user_model = user_model
        self.setStyleSheet("""
            QWidget { background-color: #F8F9FA; }
            .QFrame#CardFrame { background-color: white; border-radius: 16px; border: 1px solid #E0E0E0; }
            .QLabel#SectionTitle { font-size: 20px; font-weight: bold; color: #2E2E2E; }
            .QLabel#SettingLabel { font-size: 14px; color: #333; font-weight: bold; }
            .QLabel#DescLabel { font-size: 12px; color: #666; }
            .QCheckBox { font-size: 13px; color: #333; spacing: 8px; }
            .QCheckBox::indicator { width: 18px; height: 18px; }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(0)
        
        # Title
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setStyleSheet("color: #2E2E2E; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # ===== NOTIFICATIONS SECTION =====
        self.create_notifications_section(content_layout)
        
        # ===== PRIVACY AND SECURITY SECTION =====
        self.create_privacy_section(content_layout)
        
        # Add stretch at the end
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Logout button at the bottom
        logout_container = QHBoxLayout()
        logout_container.setContentsMargins(0, 20, 0, 0)
        logout_container.addStretch()
        self.btn_logout = QPushButton("Log Out")
        self.btn_logout.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_logout.setFixedHeight(48)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                padding: 0 32px;
            }
            QPushButton:hover {
                background-color: #B71C1C;
            }
        """)
        self.btn_logout.clicked.connect(self.on_logout_clicked)
        logout_container.addWidget(self.btn_logout)
        main_layout.addLayout(logout_container)
    
    def create_notifications_section(self, parent_layout):
        """Create notifications settings section"""
        card = QFrame()
        card.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)
        
        # Section title
        title = QLabel("🔔 Notifications")
        title.setObjectName("SectionTitle")
        card_layout.addWidget(title)
        
        # Email notifications checkbox
        email_container = QHBoxLayout()
        email_container.setSpacing(15)
        
        self.email_checkbox = QCheckBox()
        self.email_checkbox.setChecked(False)
        self.email_checkbox.stateChanged.connect(self.on_settings_changed)
        
        email_label_layout = QVBoxLayout()
        email_label_layout.setSpacing(2)
        email_label_layout.setContentsMargins(0, 0, 0, 0)
        
        email_title = QLabel("Email Notifications")
        email_title.setObjectName("SettingLabel")
        email_desc = QLabel("Receive task reminders via email")
        email_desc.setObjectName("DescLabel")
        
        email_label_layout.addWidget(email_title)
        email_label_layout.addWidget(email_desc)
        
        email_container.addWidget(self.email_checkbox)
        email_container.addLayout(email_label_layout, 1)
        email_container.addStretch()
        
        card_layout.addLayout(email_container)
        
        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setStyleSheet("background-color: #EEE;")
        card_layout.addWidget(separator1)
        
        # Push notifications checkbox
        push_container = QHBoxLayout()
        push_container.setSpacing(15)
        
        self.push_checkbox = QCheckBox()
        self.push_checkbox.setChecked(False)
        self.push_checkbox.stateChanged.connect(self.on_settings_changed)
        
        push_label_layout = QVBoxLayout()
        push_label_layout.setSpacing(2)
        push_label_layout.setContentsMargins(0, 0, 0, 0)
        
        push_title = QLabel("Push Notifications")
        push_title.setObjectName("SettingLabel")
        push_desc = QLabel("Receive push notifications even when app is closed")
        push_desc.setObjectName("DescLabel")
        
        push_label_layout.addWidget(push_title)
        push_label_layout.addWidget(push_desc)
        
        push_container.addWidget(self.push_checkbox)
        push_container.addLayout(push_label_layout, 1)
        push_container.addStretch()
        
        card_layout.addLayout(push_container)
        
        parent_layout.addWidget(card)
    
    def create_privacy_section(self, parent_layout):
        """Create privacy and security settings section"""
        card = QFrame()
        card.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)
        
        # Section title
        title = QLabel("🔐 Privacy & Security")
        title.setObjectName("SectionTitle")
        card_layout.addWidget(title)
        
        # Change password section
        pwd_container = QHBoxLayout()
        pwd_container.setSpacing(15)
        
        pwd_label_layout = QVBoxLayout()
        pwd_label_layout.setSpacing(2)
        pwd_label_layout.setContentsMargins(0, 0, 0, 0)
        
        pwd_title = QLabel("Change Password")
        pwd_title.setObjectName("SettingLabel")
        pwd_desc = QLabel("Update your account password")
        pwd_desc.setObjectName("DescLabel")
        
        pwd_label_layout.addWidget(pwd_title)
        pwd_label_layout.addWidget(pwd_desc)
        
        self.btn_change_password = QPushButton("Change Password")
        self.btn_change_password.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_change_password.setFixedHeight(40)
        self.btn_change_password.setFixedWidth(150)
        self.btn_change_password.setStyleSheet("""
            QPushButton {
                background-color: #FF6F00;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E65100;
            }
        """)
        self.btn_change_password.clicked.connect(self.on_change_password_clicked)
        
        pwd_container.addLayout(pwd_label_layout, 1)
        pwd_container.addWidget(self.btn_change_password)
        
        card_layout.addLayout(pwd_container)
        
        parent_layout.addWidget(card)
    
    def on_settings_changed(self):
        """Emit signal when settings change"""
        settings = {
            'email_notifications': self.email_checkbox.isChecked(),
            'push_notifications': self.push_checkbox.isChecked()
        }
        self.settings_changed.emit(settings)
    
    def on_change_password_clicked(self):
        """Show the change password popup dialog"""
        print(f"DEBUG DisplaySettings: user_model = {self.user_model}")
        print(f"DEBUG DisplaySettings: user_model type = {type(self.user_model)}")
        if self.user_model:
            print(f"DEBUG DisplaySettings: username = {self.user_model.getUsername()}, id = {self.user_model.getUserID()}")
        
        self.password_popup = ChangePasswordPopUp(self.user_model, self)
        self.password_popup.password_changed.connect(self.handle_password_change)
        self.password_popup.exec_()
    
    def handle_password_change(self, new_password: str, confirm_password: str):
        """Handle password change from popup"""
        self.password_changed.emit(new_password, confirm_password)
    
    def set_notification_settings(self, email_enabled, push_enabled):
        """Load and display saved notification settings"""
        self.email_checkbox.blockSignals(True)
        self.push_checkbox.blockSignals(True)
        
        self.email_checkbox.setChecked(email_enabled)
        self.push_checkbox.setChecked(push_enabled)
        
        self.email_checkbox.blockSignals(False)
        self.push_checkbox.blockSignals(False)

    def on_logout_clicked(self):
        """Emit logout request to parent container"""
        self.logoutRequested.emit()
