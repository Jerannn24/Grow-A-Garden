import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QSystemTrayIcon, QMenu, QAction, QStyle, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Optional

from models.UserModel import UserModel 
from models.Task import Task
from views.FormLogin import LoginForm       
from views.FormRegister import RegisterForm  
from views.FormChangePassword import ChangePasswordForm
from views.HomeScreen import MainWindow
from views.DisplayNotification import DisplayNotification
from controllers.NotificationManager import NotificationManager

class AccountManager(QWidget):
    profileUpdateResponse = pyqtSignal(str, bool)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grow a Garden Application - Account Manager")
        self.setWindowState(Qt.WindowMaximized)
        
        self.stackWidget = QStackedWidget()
        self.widgets = {}
        self.notification_manager = None
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.stackWidget)
        
        self.model = UserModel()
        self.currentUser: UserModel = None 
        conn = self.model.get_conn()
        self.model.createTable(conn)
        
        # Initialize Task table
        Task.init_table()
        self._initViews()
        
        self.switchView('login')
        
        # --- System Tray Icon for main application ---
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setToolTip("Grow a Garden")

        tray_menu = QMenu()
        action_show = QAction("Open Garden", self)
        action_show.triggered.connect(self.show_window)
        action_quit = QAction("Quit Application", self)
        action_quit.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(action_show)
        tray_menu.addAction(action_quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

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
        
        self.homeScreenView.profile_page.profileUpdateRequested.connect(self.handleProfileUpdateRequest)
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
            if hasattr(self, 'notification_manager') and self.notification_manager:
                try:
                    self.notification_manager.timer.stop()
                except Exception:
                    pass
            self.notification_manager = NotificationManager(self.currentUser)
            self.notification_manager.newNotification.connect(lambda notifID, title, msg: self._dispatch_notification(notifID, title, msg))
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
            
    def handleProfileUpdateRequest(self, username, email, location, profileInfo):
        if self.currentUser is None:
            self.profileUpdateResponse.emit("Error: User not logged in.", False)
            return

        user_id = self.currentUser.getUserID()
        
        success, message = UserModel.updateProfil(
            self.model,
            user_id,
            username, 
            email, 
            location,
            profileInfo)
        
        if success:
            self.currentUser = UserModel.getByID(user_id) 
            
            if self.homeScreenView:
                self.homeScreenView.set_current_user(self.currentUser)
                
            print(f"Success to Update Profile for: {username}.")
            self.profileUpdateResponse.emit("Profil berhasil diperbarui!", True)
        else:
            print(f"Failed to Update Profile: {message}")
            self.profileUpdateResponse.emit(message, False)
            
    def handleLogoutRequest(self):
        self.currentUser = None
        print("Logout Success.")
        self.switchView('login')
        if self.notification_manager:
            try:
                self.notification_manager.timer.stop()
            except Exception:
                pass
            self.notification_manager = None

    def show_notification_popup(self, title, message, notifID=None):
        """Show a popup notification or a system tray balloon depending on visibility."""
        if self.isVisible():
            popup = DisplayNotification.show_notification(title, message, self)
            geo = self.geometry()
            x = geo.x() + geo.width() - popup.width() - 20
            y = geo.y() + geo.height() - popup.height() - 20
            popup.move(x, y)
            popup.show()
            if notifID:
                try:
                    from models.TaskNotification import TaskNotification
                    TaskNotification.mark_as_sended(notifID)
                except Exception:
                    pass
        else:
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 5000)
        if notifID:
            try:
                from models.TaskNotification import TaskNotification
                TaskNotification.mark_as_sended(notifID)
            except Exception:
                pass

    def _dispatch_notification(self, notifID, title, message):
        if hasattr(self, 'homeScreenView') and self.stackWidget.currentWidget() == self.homeScreenView:
            try:
                self.homeScreenView.receiveNotif(title, message, notifID)
                return
            except Exception:
                pass
        self.show_notification_popup(title, message, notifID)

    
    def switchView(self, viewName):
        if viewName in self.widgets:
            targetWidget = self.widgets[viewName]
            self.stackWidget.setCurrentWidget(targetWidget)
            self.setWindowTitle(targetWidget.windowTitle())
        else:
            print(f"Error: View '{viewName}' not Found. Pls add a view.")

    def show_window(self):
        self.show()
        self.setWindowState(Qt.WindowNoState)
        self.raise_()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_window()

    def closeEvent(self, event):
        self.hide()
        self.tray_icon.showMessage("Grow a Garden", "App is running in background.")
        event.ignore()