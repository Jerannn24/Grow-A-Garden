import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect,
    QMessageBox # <-- Diperlukan untuk Pop-up
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QByteArray, pyqtSignal, QSize, QTimer 

class ChangePasswordForm(QWidget):
    switchToLoginRequested = pyqtSignal() 
    changePasswordRequested = pyqtSignal(str, str, str, str)
    error_display = pyqtSignal(str) 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grow a Garden - Change Password")
        
        self.setStyleSheet("background-color: #f7f7f7;")

        mainLayout = QHBoxLayout(self)
        
        self.inputUsername = QLineEdit()
        self.inputEmail = QLineEdit()
        self.inputNewPass = QLineEdit()
        self.inputConfirmPass = QLineEdit()
        self.changeButton = QPushButton()
        self.backLinkWidget = QLabel()
        
        self.errorLabel = QLabel("") 
        
        self.forgotLink = QLabel("")
        self.leftPanel = self._createLeftPanel()
        mainLayout.addWidget(self.leftPanel, 1) 
        
        self.rightPanel = self._createRightPanel()
        mainLayout.addWidget(self.rightPanel, 1)
        
        self._setupConnections()

    def displayError(self, message):
        """Menampilkan pop-up error yang diperlebar dan berpusat, dengan gaya modern."""
        
        msgBox = QMessageBox() 
        
        msgBox.setIcon(QMessageBox.NoIcon) 
        msgBox.setWindowTitle("Reset Password Failed")
        msgBox.setText("❌ Penggantian Kata Sandi Gagal")
        msgBox.setInformativeText(message) 
        msgBox.setStandardButtons(QMessageBox.Ok)
        
        msgBox.setFixedSize(QSize(600, 250)) 
        
        msgBox.setStyleSheet("""
            QMessageBox {
                background-color: white; 
                border: none; 
                border-radius: 16px; 
                padding: 15px;
                color: #333333; 
                font-family: 'Geist', sans-serif;
            }
            
            /* Area pesan utama */
            QMessageBox::message {
                padding: 15px 30px 15px 30px; 
                border-left: 5px solid #e53935; /* Garis aksen merah di kiri */
                margin-left: 0px; 
                margin-top: 10px;
                margin-bottom: 20px;
                background-color: #fffafa; 
            }

            QMessageBox QLabel {
                color: #444444; 
                font-size: 14px;
                padding: 0;
            }
            
            /* Judul/Teks utama */
            QMessageBox QLabel:first-child {
                color: #e53935; 
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            
            QMessageBox QPushButton {
                background-color: #e53935; 
                color: white;
                border-radius: 8px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QMessageBox QPushButton:hover {
                background-color: #c62828; 
            }
        """)

        shadow = QGraphicsDropShadowEffect(msgBox)
        shadow.setBlurRadius(40) 
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        msgBox.setGraphicsEffect(shadow)

        msgBox.exec_() 
    
    def _createLeftPanel(self):
        frame = QFrame()
        frame.setStyleSheet("background-color: #f7f7f7;")
        
        frameLayout = QVBoxLayout(frame)
        frameLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        frameLayout.setContentsMargins(65, 55, 65, 50)
        
        iconSize = 160
        svgFilePath = "src/public/icon.svg" 
        
        iconToAdd = None 
        svgWidget = QSvgWidget() 
        
        try:
            with open(svgFilePath, 'rb') as f:
                 svgData = f.read()
            svgWidget.load(QByteArray(svgData))
        except FileNotFoundError:
            svgWidget = None
        
        if svgWidget and svgWidget.renderer().isValid():
            iconToAdd = svgWidget
            iconToAdd.setFixedSize(iconSize, iconSize)
        else:
            fallbackLabel = QLabel("⚠️ SVG Not Found") 
            fallbackLabel.setFont(QFont('Geist', 12))
            iconToAdd = fallbackLabel
        
        iconLayout = QVBoxLayout()
        iconLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        iconLayout.addWidget(iconToAdd, alignment=Qt.AlignCenter)
        frameLayout.addLayout(iconLayout)
        
        appTitle = QLabel("Grow a Garden")
        appTitle.setFont(QFont('Geist', 48, QFont.Bold))
        appTitle.setStyleSheet("padding-top: 24px;")
        frameLayout.addWidget(appTitle)

        appDesc = QLabel("Grow your dream garden with ease")
        appDesc.setFont(QFont('Geist', 20))
        appDesc.setStyleSheet("padding-bottom: 32px;  color:#636363;")
        frameLayout.addWidget(appDesc)
        
        frameLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))

        def createFeatureItem(iconText, title, description,r,g,b,opacity):
            featureWidget = QWidget()
            featureLayout = QHBoxLayout(featureWidget)
            featureLayout.setContentsMargins(0, 5, 0, 5)
            
            iconPlaceholder = QLabel(iconText) 
            iconPlaceholder.setFont(QFont('Geist', 16))
            
            iconPlaceholder.setStyleSheet(f"""
                QLabel {{
                    background-color: rgba({r},{g},{b},{opacity});
                    border-radius: 8px;
                    padding: 8px; 
                    margin-right: 10px;
                    min-width: 48px;
                    max-width: 48px;
                    min-height: 48px;
                    max-height: 48px;
                }}
                """)

            iconPlaceholder.setAlignment(Qt.AlignCenter)
            
            featureLayout.addWidget(iconPlaceholder)
            
            textVBox = QVBoxLayout()
            titleLabel = QLabel(title)
            titleLabel.setFont(QFont('Geist', 12, QFont.Bold))
            descLabel = QLabel(description)
            descLabel.setFont(QFont('Geist', 11))
            
            textVBox.addWidget(titleLabel)
            textVBox.addWidget(descLabel)
            featureLayout.addLayout(textVBox)
            
            return featureWidget
        descLayout = QVBoxLayout()
        descLayout.setSpacing(24)
        descLayout.addWidget(createFeatureItem("🌱", "Plant Tracker", "Monitor the growth of each plant in detail", 7, 104, 4, 0.1))
        descLayout.addWidget(createFeatureItem("✅", "Todo List", "Schedule your gardening tasks and maintenance", 162, 165, 68, 0.1))
        descLayout.addWidget(createFeatureItem("📊", "Insights", "Get recommendations based on your garden history", 145, 85, 0, 0.1))
        
        descLayout.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        frameLayout.addLayout(descLayout)
        return frame
    # ------------------------------------------------
    
    def _createRightPanel(self):
        centerWidget = QWidget()
        centerLayout = QVBoxLayout(centerWidget)
        centerLayout.setAlignment(Qt.AlignCenter)

        frame = QFrame()
        frame.setMaximumWidth(760) 
        
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 24px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 80)) 
        frame.setGraphicsEffect(shadow)
        
        formLayout = QVBoxLayout(frame)
        formLayout.setContentsMargins(50, 65, 50, 65)
        
        title = QLabel("Reset Kata Sandi")
        title.setFont(QFont('Geist', 28, QFont.Bold)) 
        formLayout.addWidget(title)
        
        subtitle = QLabel("Masukkan detail untuk mengatur ulang kata sandi")
        subtitle.setStyleSheet("color: #666; margin-bottom: 25px;")
        formLayout.addWidget(subtitle)
        
        # errorLabel tidak ditampilkan di layout (diganti pop-up)
        # self.errorLabel.setStyleSheet("color: red; margin-bottom: 10px; font-weight: bold;")
        # formLayout.addWidget(self.errorLabel) 
        
        def createFormField(labelText, placeholderText, isPassword=False, lineEditObject=None):
            label = QLabel(labelText)
            inputLine = lineEditObject if lineEditObject is not None else QLineEdit()
            inputLine.setPlaceholderText(placeholderText)
            if isPassword:
                inputLine.setEchoMode(QLineEdit.Password)
            
            inputLine.setStyleSheet("""
                QLineEdit {
                    padding: 14px;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    background-color: #f0f0f0;
                    margin-bottom: 15px;
                }
                QLineEdit:focus {
                    border: 1px solid #076804;
                    background-color: white;
                }
            """)
            
            return label, inputLine

        labelUsername, _ = createFormField("Username", "your_username", lineEditObject=self.inputUsername)
        formLayout.addWidget(labelUsername)
        formLayout.addWidget(self.inputUsername)
        
        labelEmail, _ = createFormField("Email", "nama@contoh.com", lineEditObject=self.inputEmail)
        formLayout.addWidget(labelEmail)
        formLayout.addWidget(self.inputEmail)
        
        labelNewPass, _ = createFormField("Kata Sandi Baru", "Masukkan kata sandi baru", isPassword=True, lineEditObject=self.inputNewPass)
        formLayout.addWidget(labelNewPass)
        formLayout.addWidget(self.inputNewPass)

        labelConfirmPass, _ = createFormField("Konfirmasi Kata Sandi Baru", "Konfirmasi kata sandi baru", isPassword=True, lineEditObject=self.inputConfirmPass)
        formLayout.addWidget(labelConfirmPass)
        formLayout.addWidget(self.inputConfirmPass)
        
        self.changeButton.setText("Reset Kata Sandi")
        self.changeButton.setFont(QFont('Geist', 14, QFont.Bold))
        
        self.changeButton.setStyleSheet("""
            QPushButton {
                background-color: #076804;
                color: white;
                padding: 15px;
                border-radius: 8px;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            QPushButton:hover {
                background-color: #054803;
            }
        """)
        
        self.changeButton.setCursor(Qt.PointingHandCursor)
        
        formLayout.addWidget(self.changeButton)
        
        self.backLinkWidget = QLabel('<a href="#" style="color: #076804; text-decoration: none;">Back To Sign In</a>')
        self.backLinkWidget.setOpenExternalLinks(False)
        self.backLinkWidget.setAlignment(Qt.AlignCenter)
        self.backLinkWidget.setCursor(Qt.PointingHandCursor)
        
        formLayout.addWidget(self.backLinkWidget)
        formLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        centerLayout.addWidget(frame)
        return centerWidget

    def _setupConnections(self):
        self.error_display.connect(self.displayError) 
        
        self.changeButton.clicked.connect(lambda: 
            self.changePasswordRequested.emit(
                self.inputUsername.text(),     
                self.inputEmail.text(),      
                self.inputNewPass.text(),      
                self.inputConfirmPass.text()  
            )
        )
        self.backLinkWidget.linkActivated.connect(lambda: self.switchToLoginRequested.emit())
        
    def clearForm(self):
        self.inputUsername.clear()
        self.inputEmail.clear()
        self.inputNewPass.clear()
        self.inputConfirmPass.clear()
        self.errorLabel.clear() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChangePasswordForm()
    window.showMaximized() 
    
    def handle_change_password(username, email, new_pass, confirm_pass):
        print(f"Password reset attempt for: {username}, {email}")
        
        if new_pass != confirm_pass:
            message = "Kata Sandi Baru dan Konfirmasi Kata Sandi tidak cocok. Mohon ulangi."
        elif len(new_pass) < 6:
            message = "Kata Sandi harus memiliki minimal 6 karakter."
        else:
            message = "Username atau Email tidak ditemukan dalam sistem kami."
            
        QTimer.singleShot(500, lambda: window.error_display.emit(message))

    window.changePasswordRequested.connect(handle_change_password)
    # --------------------------------------------------------------

    sys.exit(app.exec_())