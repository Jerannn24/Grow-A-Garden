import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFrame, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from models.UserModel import UserModel # Membutuhkan class UserModel

class FormChangeProfile(QDialog):
    profileUpdateRequested = pyqtSignal(str, str, str, str)
    messageDisplay = pyqtSignal(str, bool) 

    def __init__(self, current_user: UserModel, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.setWindowTitle("Edit Your Profile")
        self.setFixedWidth(500)
        
        self.setObjectName("ProfileDialog")
        self.setStyleSheet(self._get_stylesheet())

        self.setup_ui()
        self._load_current_data()
        self._connect_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        title_lbl = QLabel("Edit Profile Details")
        title_lbl.setFont(QFont("Arial", 18, QFont.Bold))
        title_lbl.setStyleSheet("color: #2E7D32;")
        main_layout.addWidget(title_lbl, alignment=Qt.AlignCenter)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #E0E0E0;")
        main_layout.addWidget(separator)

        self.inputUsername = self._create_input_field("Username:", "Enter new username", False)

        self.inputEmail = self._create_input_field("Email:", "Enter new email", False)
        
        self.inputLocation = self._create_input_field("Location:", "Enter your location", False)

        self.infoLabel = QLabel("Profile Info (About Me):")
        self.infoLabel.setStyleSheet("font-weight: bold; color: #4CAF50;")
        self.inputProfileInfo = QTextEdit()
        self.inputProfileInfo.setFixedHeight(100)
        self.inputProfileInfo.setPlaceholderText("Tell us about yourself...")
        self.inputProfileInfo.setObjectName("ProfileInfoText")
        main_layout.addWidget(self.infoLabel)
        main_layout.addWidget(self.inputProfileInfo)
        
        self.errorLabel = QLabel("")
        self.errorLabel.setStyleSheet("color: red; font-weight: bold;")
        main_layout.addWidget(self.errorLabel)

        main_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setObjectName("CancelButton")
        self.cancelButton.clicked.connect(self.reject) 
        
        self.saveButton = QPushButton("Save Changes")
        self.saveButton.setObjectName("SaveButton")
        self.saveButton.clicked.connect(self._validate_and_emit) 
        self.saveButton.clicked.connect(self.reject)
        
        button_layout.addWidget(self.cancelButton)
        button_layout.addWidget(self.saveButton)
        
        main_layout.addLayout(button_layout)

    def _create_input_field(self, label_text, placeholder, is_password):
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)
        line_edit.setObjectName("InputLineEdit")
        
        self.layout().addWidget(label)
        self.layout().addWidget(line_edit)
        return line_edit
        
    def _load_current_data(self):
        if self.current_user:
            self.inputUsername.setText(self.current_user.getUsername())
            self.inputEmail.setText(self.current_user.getEmail())
            self.inputLocation.setText(self.current_user.getLocation())
            self.inputProfileInfo.setText(self.current_user.getProfileInfo())
        
    def _validate_and_emit(self):
        username = self.inputUsername.text().strip()
        email = self.inputEmail.text().strip()
        location = self.inputLocation.text().strip()
        profile_info = self.inputProfileInfo.toPlainText().strip()
        
        if not username or not email:
            self.errorLabel.setText("Username and Email cannot be empty.")
            return

        self.profileUpdateRequested.emit(username, email, location, profile_info)

    def display_message(self, message: str, is_success: bool):
        if is_success:
            self.errorLabel.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.errorLabel.setStyleSheet("color: red; font-weight: bold;")
            
        self.errorLabel.setText(message)
        
        if is_success:
            QMessageBox.information(self, "Success", message)
            self.accept()
            
    def _connect_signals(self):
        self.saveButton.clicked.connect(self._validate_and_emit) 
        
    def _validate_and_emit(self):
        username = self.inputUsername.text().strip()
        email = self.inputEmail.text().strip()
        location = self.inputLocation.text().strip()
        profile_info = self.inputProfileInfo.toPlainText().strip()
        
        if not username or not email:
            self.errorLabel.setText("Username and Email cannot be empty.")
            return

        self.profileUpdateRequested.emit(username, email, location, profile_info)
        
    def _get_stylesheet(self):
        return """
            QDialog#ProfileDialog {
                background-color: #f0f0f0;
                border-radius: 15px;
            }
            QLabel {
                font-size: 11pt;
            }
            QLineEdit#InputLineEdit, QTextEdit#ProfileInfoText {
                padding: 8px;
                border: 1px solid #C8E6C9;
                border-radius: 8px;
                font-size: 10pt;
                background-color: white;
            }
            QLineEdit#InputLineEdit:focus, QTextEdit#ProfileInfoText:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton#SaveButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#SaveButton:hover {
                background-color: #66BB6A;
            }
            QPushButton#CancelButton {
                background-color: #E0E0E0;
                color: #4A4A4A;
            }
            QPushButton#CancelButton:hover {
                background-color: #CCCCCC;
            }
        """

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    class MockUser:
        def getUsername(self): return "MawarMelati"
        def getEmail(self): return "mawar@example.com"
        def getLocation(self): return "Bandung, Indonesia"
        def getProfileInfo(self): return "I enjoy gardening and planting red roses!"

    app = QApplication(sys.argv)
    mock_user = MockUser()
    
    dialog = FormChangeProfile(mock_user)
    
    def handle_update(u, e, l, i):
        print(f"Update Requested: U:{u}, E:{e}, L:{l}, I:{i}")
        if "fail" in u.lower():
            dialog.display_message("Simulasi GAGAL: Username mengandung kata terlarang.", False)
        else:
            dialog.display_message("Simulasi SUKSES: Data profil telah diperbarui!", True)

    dialog.profileUpdateRequested.connect(handle_update)
    
    dialog.exec_()
    sys.exit(app.exec_())