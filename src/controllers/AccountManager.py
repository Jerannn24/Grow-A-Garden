# File: controller/account_manager.py

import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt

# Import Model
from models.UserModel import UserModel 

# Import Views 
from views.FormLogin import LoginForm        
from views.FormRegister import RegisterForm  

class AccountManager(QWidget): # <-- Nama kelas diubah sesuai permintaan
    """
    Mengelola QStackedWidget, menghubungkan View dan Model.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grow a Garden Application - Account Manager")
        self.setWindowState(Qt.WindowMaximized)
        
        self.stackWidget = QStackedWidget()
        self.widgets = {}
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.stackWidget)
        
        # 1. Inisialisasi Model
        self.model = UserModel() 
        
        # 2. Inisialisasi Views dan Hubungkan
        self._initViews()
        
        self.switchView('login')

    def _initViews(self):
        """Membuat View dan mengatur koneksi sinyal-slot."""
        
        self.loginView = LoginForm()
        self.stackWidget.addWidget(self.loginView)
        self.widgets['login'] = self.loginView
        
        self.registerView = RegisterForm()
        self.stackWidget.addWidget(self.registerView)
        self.widgets['register'] = self.registerView
        
        
        self.loginView.switchToRegisterRequested.connect(lambda: self.switchView('register'))
        self.registerView.switchToLoginRequested.connect(lambda: self.switchView('login')) 
        
        self.loginView.loginRequested.connect(self.handleLoginRequest)
        self.registerView.registerRequested.connect(self.handleRegisterRequest) 


    def handleLoginRequest(self, email, password):
        """Menerima input dari LoginView, memanggil Model, dan mengarahkan tampilan."""
        print(email, " ", password)
        success, message = self.model.loginUser(email.strip(), password.strip())
        
        self.loginView.clearForm()

        if success:
            userData = self.model.getCurrentUser()
            print(f"✅ Login Sukses untuk: {userData['username']}. Pindah ke Homescreen.")
            
            # TODO: Tambahkan HomeView ke self.widgets dan gunakan:
            # self.switchView('homescreen') 
            
        else:
             print(f"{message}")

    def handleRegisterRequest(self, username, email, password, location, confirmPassword):
        """Menerima input dari RegisterView, memanggil Model."""
        success, message = self.model.registerUser(username.strip(), email.strip(), password.strip(), location.strip(), confirmPassword.strip())
        
        if success:
            print(f"✅ Registrasi Sukses untuk: {username}. Beralih ke Login.")
            
            self.registerView.clearForm()
            self.switchView('login')
            
        else:
            print(f"{message}")
    # --- View Manager ---
    
    def switchView(self, viewName):
        """Mengganti tampilan yang ditampilkan di QStackedWidget."""
        if viewName in self.widgets:
            targetWidget = self.widgets[viewName]
            self.stackWidget.setCurrentWidget(targetWidget)
            self.setWindowTitle(targetWidget.windowTitle())
        else:
            print(f"Error: View '{viewName}' tidak ditemukan. Mohon tambahkan HomescreenView.")