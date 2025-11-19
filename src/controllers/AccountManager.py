# File: controller/AccountManager.py

import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from typing import Optional

# Import Model
from models.UserModel import UserModel 
# Import Views 
from views.FormLogin import LoginForm        
from views.FormRegister import RegisterForm  

class AccountManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grow a Garden Application - Account Manager")
        self.setWindowState(Qt.WindowMaximized)
        
        self.stackWidget = QStackedWidget()
        self.widgets = {}
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.stackWidget)
        
        self.model = UserModel()
        self.currentUser: Optional[UserModel] = None 
        
        self._initViews()
        
        self.switchView('login')

    def _initViews(self):
        self.loginView = LoginForm()
        self.stackWidget.addWidget(self.loginView)
        self.widgets['login'] = self.loginView
        
        self.registerView = RegisterForm()
        self.stackWidget.addWidget(self.registerView)
        self.widgets['register'] = self.registerView

        self.loginView.switchToRegisterRequested.connect(lambda: self.switchView('register'))
        self.loginView.loginRequested.connect(self.handleLoginRequest)
        
        self.registerView.switchToLoginRequested.connect(lambda: self.switchView('login'))
        self.registerView.registerRequested.connect(self.handleRegisterRequest)

    
    def handleLoginRequest(self, email, password):        
        user_instance, message = self.model.loginUser(email.strip(), password.strip())
        
        self.loginView.clearForm()

        if user_instance:
            self.currentUser = user_instance
            print(f"✅ Login Sukses untuk: {self.currentUser.username} (ID: {self.currentUser.userID}). Pindah ke Homescreen.")
                        
        else:
             print(f"❌ Login Gagal: {message}")
             self.loginView.errorDisplay.emit(message)


    def handleRegisterRequest(self, username, email, password, location, confirmPassword):
        success, message = self.model.registerUser(username.strip(), email.strip(), password.strip(), location.strip(), confirmPassword.strip())
        
        if success:
            print(f"✅ Registrasi Sukses untuk: {username}. Beralih ke Login.")
            
            self.registerView.clearForm()
            self.switchView('login')
            
        else:
            print(f"❌ Registrasi Gagal: {message}")
            self.registerView.errorDisplay.emit(message)
            
    def handleLogoutRequest(self):
        self.currentUser = None
        print("Pengguna berhasil logout.")
        self.switchView('login')

    
    def switchView(self, viewName):
        """Mengganti tampilan yang ditampilkan di QStackedWidget."""
        if viewName in self.widgets:
            targetWidget = self.widgets[viewName]
            self.stackWidget.setCurrentWidget(targetWidget)
            self.setWindowTitle(targetWidget.windowTitle())
        else:
            print(f"Error: View '{viewName}' tidak ditemukan. Mohon tambahkan HomescreenView.")