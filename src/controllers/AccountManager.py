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
from views.FormChangePassword import ChangePasswordForm
from views.HomeScreen import MainWindow

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

        self.homeScreenView = MainWindow()
        self.stackWidget.addWidget(self.homeScreenView)
        self.widgets['homescreen'] = self.homeScreenView
        
        self.changePasswordView = ChangePasswordForm()
        self.stackWidget.addWidget(self.changePasswordView)
        self.widgets['changepassword'] = self.changePasswordView
        
        self.loginView.switchToHomeScreen.connect(lambda: self.switchView('homescreen'))
        self.loginView.switchToRegisterRequested.connect(lambda: self.switchView('register'))
        self.loginView.switchToChangePassword.connect(lambda: self.switchView('changepassword'))
        self.loginView.loginRequested.connect(self.handleLoginRequest)

        self.changePasswordView.switchToLoginRequested.connect(lambda: self.switchView('login'))
        self.changePasswordView.changePasswordRequested.connect(self.handleChangePasswordRequest)

        self.registerView.switchToLoginRequested.connect(lambda: self.switchView('login'))
        self.registerView.registerRequested.connect(self.handleRegisterRequest)
        
        self.homeScreenView.logoutRequested.connect(self.handleLogoutRequest) 

    
    def handleLoginRequest(self, email, password):        
        user_instance, message = self.model.loginUser(email.strip(), password.strip())
        
        self.loginView.clearForm()

        if user_instance:
            self.currentUser = user_instance
            self.homeScreenView.set_current_user(self.currentUser)
            self.switchView('homescreen')
            print(f"Login Success : {self.currentUser.username} (ID: {self.currentUser.userID}). Pindah ke Homescreen.")
                        
        else:
             print(f"Login Gagal: {message}")
             self.loginView.errorDisplay.emit(message)


    def handleRegisterRequest(self, username, email, password, location, confirmPassword):
        success, message = self.model.registerUser(username.strip(), email.strip(), password.strip(), location.strip(), confirmPassword.strip())
        
        if success:
            print(f"Registrasi Sukses untuk: {username}. Beralih ke Login.")
            
            self.registerView.clearForm()
            self.switchView('login')
            
        else:
            print(f"Registrasi Gagal: {message}")
            self.registerView.errorDisplay.emit(message)
    
    def handleChangePasswordRequest(self, username, email, newPassword, confirmPassword):
        success, message = self.model.changePassword(username, email, newPassword, confirmPassword)
        
        if success:
            print(f"Success To Change Password : {username}. To Login.")
            
            self.changePasswordView.clearForm()
            self.switchView('login')
        
        else:
            print(f"Failed to Change Password : {message}")
            self.registerView.errorDisplay.emit(message)
            
         
    def handleLogoutRequest(self):
        self.currentUser = None
        print("Logout Success.")
        self.switchView('login')

    
    def switchView(self, viewName):
        if viewName in self.widgets:
            targetWidget = self.widgets[viewName]
            self.stackWidget.setCurrentWidget(targetWidget)
            self.setWindowTitle(targetWidget.windowTitle())
        else:
            print(f"Error: View '{viewName}' not Found. Pls add a view.")