import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QByteArray, pyqtSignal


class LoginForm(QWidget):
    switchToRegisterRequested = pyqtSignal() 
    loginRequested = pyqtSignal(str, str)
    errorDisplay = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grow a Garden - Login")
        
        self.setStyleSheet("background-color: #f7f7f7;")

        mainLayout = QHBoxLayout(self)
        
        self.leftPanel = self._createLeftPanel()
        mainLayout.addWidget(self.leftPanel, 1) 
        
        self.rightPanel = self._createRightPanel()
        mainLayout.addWidget(self.rightPanel, 1)
        self.inputEmail = QLineEdit()
        self.inputPass = QLineEdit() 
        self.loginButton = QPushButton() 
        self.signupLink = QLabel() 
        
        self.errorLabel = QLabel("")
        self.errorLabel.setStyleSheet("color: red; margin-bottom: 10px;")
        
        self._setupConnections()
       
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
        svgWidget.load(svgFilePath)
        
        if svgWidget.renderer().isValid():
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
        
        title = QLabel("Sign In")
        title.setFont(QFont('Geist', 28, QFont.Bold)) 
        formLayout.addWidget(title)
        
        subtitle = QLabel("Welcome back to your garden")
        subtitle.setStyleSheet("color: #666; margin-bottom: 25px;")
        formLayout.addWidget(subtitle)
        
        def createFormField(labelText, placeholderText, isPassword=False):
            label = QLabel(labelText)
            inputLine = QLineEdit()
            inputLine.setPlaceholderText(placeholderText)
            if isPassword:
                inputLine.setEchoMode(QLineEdit.Password)
            
            # Styling Input Field
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

        # Email (menggunakan placeholder Bahasa Indonesia)
        labelEmail, inputEmail = createFormField("Email", "nama@example.com")
        formLayout.addWidget(labelEmail)
        formLayout.addWidget(inputEmail)
        
        # Password (menggunakan label Bahasa Indonesia)
        labelPass, inputPass = createFormField("Password", "••••••••", isPassword=True)
        formLayout.addWidget(labelPass)
        formLayout.addWidget(inputPass)
        
        # Tombol Login
        loginButton = QPushButton("Sign In")
        loginButton.setFont(QFont('Geist', 14, QFont.Bold))
        
        # Styling Tombol
        loginButton.setStyleSheet("""
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
        
        loginButton.setCursor(Qt.PointingHandCursor)
        loginButton.clicked.connect(lambda: 
            self.loginRequested.emit(inputEmail.text(), inputPass.text())
        )
        formLayout.addWidget(loginButton)
        # Link Lupa Kata Sandi
        forgotLink = QLabel('<a href="#" style="color: #076804; text-decoration: none;">Forgot your Password?</a>')
        forgotLink.setOpenExternalLinks(True)
        forgotLink.setAlignment(Qt.AlignCenter)
        forgotLink.setCursor(Qt.PointingHandCursor)
        formLayout.addWidget(forgotLink)
        
        # Pemisah 'atau'
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("margin: 20px 0;")
        
        orLabel = QLabel("atau")
        orLabel.setAlignment(Qt.AlignCenter)
        orLayout = QHBoxLayout()
        orLayout.addWidget(separator)
        orLayout.addWidget(orLabel)
        orLayout.addWidget(separator)
        
        formLayout.addLayout(orLayout)
        
        signupLink = QLabel("Don't have an account? <a href='#' style='color: #076804; text-decoration: none;'>Sign up now</a>")
        signupLink.setOpenExternalLinks(False) 
        signupLink.setAlignment(Qt.AlignCenter)
        signupLink.setCursor(Qt.PointingHandCursor)
        signupLink.linkActivated.connect(self.switchToRegisterRequested.emit)
        formLayout.addWidget(signupLink)
        
        formLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.inputEmail = inputEmail 
        self.inputPass = inputPass
        self.loginButton = loginButton
        self.signupLink = signupLink
        
        centerLayout.addWidget(frame)
        return centerWidget
    
    def _setupConnections(self):
        self.signupLink.linkActivated.connect(self.switchToRegisterRequested.emit) 
        
        self.loginButton.clicked.connect(lambda: 
            self.loginRequested.emit(self.inputEmail.text(), self.inputPass.text())
        )
        
    def clearForm(self):
        self.inputEmail.clear()
        self.inputPass.clear()
        self.errorLabel.clear() 
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginForm()
    window.showMaximized() 
    sys.exit(app.exec_())