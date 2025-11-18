import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QByteArray, pyqtSignal

class RegisterForm(QWidget):
    switchToLoginRequested = pyqtSignal()   
    registerRequested = pyqtSignal(str, str, str, str, str) 
    errorDisplay = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grow a Garden - Sign Up")
        
        self.setStyleSheet("background-color: #f7f7f7;")
        
        self.inputName = QLineEdit() 
        self.inputEmail = QLineEdit()
        self.inputPass = QLineEdit()
        self.inputLocation = QLineEdit()
        self.inputConfirm = QLineEdit()
        self.signupButton = QPushButton()
        self.loginLink = QLabel()
        
        self.errorLabel = QLabel("")
        self.errorLabel.setStyleSheet("color: red; margin-bottom: 10px;")
        
            
        mainLayout = QHBoxLayout(self)
        
        self.leftPanel = self._createLeftPanel()
        mainLayout.addWidget(self.leftPanel, 1) 
        
        self._setupConnections()
        self.rightPanel = self._createRightPanel()
        mainLayout.addWidget(self.rightPanel, 1)
        
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
        
        title = QLabel("Sign Up")
        title.setFont(QFont('Geist', 24, QFont.Bold))
        formLayout.addWidget(title)
        
        subtitle = QLabel("Start gardening and track your plants")
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        formLayout.addWidget(subtitle)
        
        def createFormField(labelText, placeholderText, isPassword=False):
            label = QLabel(labelText)
            inputLine = QLineEdit()
            inputLine.setPlaceholderText(placeholderText)
            if isPassword:
                inputLine.setEchoMode(QLineEdit.Password)
            
            # Styling: Input Field Modern
            inputLine.setStyleSheet("""
                QLineEdit {
                    padding: 14px;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    background-color: #f0f0f0;
                    margin-bottom: 15px;
                }
                QLineEdit:focus {
                    border: 1px solid #38761d;
                    background-color: white;
                }
            """)
            
            return label, inputLine

        # Full Name
        labelName, inputName = createFormField("Full Name", "Your Name")
        formLayout.addWidget(labelName)
        formLayout.addWidget(inputName)

        # Email
        labelEmail, inputEmail = createFormField("Email", "name@example.com")
        formLayout.addWidget(labelEmail)
        formLayout.addWidget(inputEmail)
        
        # Location
        labelLocation, inputLocation = createFormField("Location", "City, Country")
        formLayout.addWidget(labelLocation)
        formLayout.addWidget(inputLocation)

        # Password
        labelPass, inputPass = createFormField("Password", "••••••••", isPassword=True)
        formLayout.addWidget(labelPass)
        formLayout.addWidget(inputPass)
        
        # Confirm Password
        labelConfirm, inputConfirm = createFormField("Confirm Password", "••••••••", isPassword=True)
        formLayout.addWidget(labelConfirm)
        formLayout.addWidget(inputConfirm)
        
        signupButton = QPushButton("Sign Up")
        signupButton.setFont(QFont('Geist', 14, QFont.Bold))
        
        # Styling: Tombol dan Margin
        signupButton.setStyleSheet("""
            QPushButton {
                background-color: #076804;
                color: white;
                padding: 15px;
                border-radius: 8px;
                margin-top: 25px;
                margin-bottom: 25px;
            }
            QPushButton:hover {
                background-color: #274e13;
            }
        """)
        
        signupButton.setCursor(Qt.PointingHandCursor)
        signupButton.clicked.connect(lambda: 
            self.registerRequested.emit(
                self.inputName.text(),        
                self.inputEmail.text(),       
                self.inputPass.text(),        
                self.inputLocation.text(),    
                self.inputConfirm.text()      
            )
        )
        formLayout.addWidget(signupButton)
        
        loginLink = QLabel('Sudah punya akun? <a href="#" style="color: #076804; text-decoration: none;">Masuk di sini</a>')
        loginLink.setOpenExternalLinks(False) # 
        loginLink.setAlignment(Qt.AlignCenter)
        loginLink.setCursor(Qt.PointingHandCursor)
        loginLink.linkActivated.connect(self.switchToLoginRequested.emit)
        formLayout.addWidget(loginLink)
        
        formLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.inputName = inputName 
        self.inputEmail = inputEmail
        self.inputPass = inputPass
        self.inputLocation = inputLocation
        self.inputConfirm = inputConfirm
        self.signupButton = signupButton
        self.loginLink = loginLink
        centerLayout.addWidget(frame)
        return centerWidget
    
    def _setupConnections(self):
        self.loginLink.linkActivated.connect(self.switchToLoginRequested.emit)
        
        self.signupButton.clicked.connect(lambda: 
            self.registerRequested.emit(
                self.inputName.text(),        
                self.inputEmail.text(),       
                self.inputPass.text(),        
                self.inputLocation.text(),    
                self.inputConfirm.text()      
            )
        )
    
    def clearForm(self):
        """Membersihkan semua field input."""
        self.inputName.clear()
        self.inputEmail.clear()
        self.inputPass.clear()
        self.inputLocation.clear()
        self.inputConfirm.clear()
        self.errorLabel.clear() 
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegisterForm()
    window.showMaximized() 
    sys.exit(app.exec_())