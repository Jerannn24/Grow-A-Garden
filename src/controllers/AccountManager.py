import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from typing import Optional

from models.UserModel import UserModel 
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
        self.currentUser: UserModel = None 
        conn = self.model.get_conn()
        self.model.createTable(conn) 
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
        user, message = self.model.loginUser(email.strip(), password.strip())
        
        if user:
            print(f"Login Sukses untuk: {user.getUsername()}")
            self.currentUser = user
            
            if self.homeScreenView: 
                self.homeScreenView.set_current_user(user)

            self.loginView.clearForm()
            self.switchView('homescreen')
        else:
            self.loginView.errorDisplay.emit(message)
            print(f"Login Gagal: {message}")


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