from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor
from models.UserModel import UserModel


class ChangePasswordPopUp(QDialog):
    """Popup dialog for changing password"""
    
    # Signals
    password_changed = pyqtSignal(str, str)  # Emits (new_password, confirm_password)
    
    def __init__(self, user_model: UserModel = None, parent=None):
        super().__init__(parent)
        self.user_model = user_model
        self.setWindowTitle("Change Password")
        self.setModal(True)
        self.setFixedWidth(450)
        self.setStyleSheet("""
            QDialog { background-color: white; border-radius: 12px; }
            QLabel#Title { font-size: 18px; font-weight: bold; color: #212121; }
            QLabel#Description { font-size: 14px; color: #666; }
            QLabel#Label { font-size: 13px; color: #333; font-weight: bold; }
            QLineEdit { 
                border: 1px solid #DDD; 
                border-radius: 6px; 
                padding: 10px; 
                font-size: 14px;
                background-color: #F8F9FA;
            }
            QLineEdit:focus {
                border: 2px solid #FF6F00;
                background-color: white;
            }
            QLabel#ErrorLabel {
                color: #D32F2F;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel("Change Password")
        title.setObjectName("Title")
        main_layout.addWidget(title)
        
        # Description
        desc = QLabel("Enter your new password below")
        desc.setObjectName("Description")
        desc.setWordWrap(True)
        main_layout.addWidget(desc)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #EEE;")
        main_layout.addWidget(separator)
        
        # New Password Field
        pwd_label = QLabel("New Password:")
        pwd_label.setObjectName("Label")
        main_layout.addWidget(pwd_label)
        
        self.input_new_password = QLineEdit()
        self.input_new_password.setPlaceholderText("Enter new password (min 8 characters)")
        self.input_new_password.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.input_new_password)
        
        # Confirm Password Field
        confirm_label = QLabel("Confirm New Password:")
        confirm_label.setObjectName("Label")
        main_layout.addWidget(confirm_label)
        
        self.input_confirm_password = QLineEdit()
        self.input_confirm_password.setPlaceholderText("Confirm your new password")
        self.input_confirm_password.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.input_confirm_password)
        
        # Error Label
        self.error_label = QLabel()
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)
        main_layout.addWidget(self.error_label)
        
        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #DDD;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #EEEEEE;
            }
        """)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_confirm = QPushButton("Change Password")
        self.btn_confirm.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_confirm.setFixedHeight(40)
        self.btn_confirm.setStyleSheet("""
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
        self.btn_confirm.clicked.connect(self.validate_and_change)
        
        button_layout.addWidget(self.btn_cancel, 1)
        button_layout.addWidget(self.btn_confirm, 1)
        
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def validate_and_change(self):
        """Validate inputs and update password in database"""
        new_password = self.input_new_password.text()
        confirm_password = self.input_confirm_password.text()
        
        # Validation checks
        if not new_password or not confirm_password:
            self.show_error("All fields are required!")
            return
        
        if len(new_password) < 8:
            self.show_error("Password must be at least 8 characters long!")
            return
        
        if new_password != confirm_password:
            self.show_error("Passwords do not match!")
            return
        
        print(f"DEBUG: user_model = {self.user_model}")
        print(f"DEBUG: user_model type = {type(self.user_model)}")
        
        # Update password in database if user_model is provided
        if self.user_model:
            try:
                user_id = self.user_model.getUserID()
                username = self.user_model.getUsername()
                print(f"DEBUG: Updating password for user_id={user_id}, username={username}")
                
                conn = self.user_model.get_conn()
                print(f"DEBUG: Database connection established")
                
                update_query = "UPDATE users SET password = ? WHERE userID = ?"
                print(f"DEBUG: Executing query: {update_query} with values (password, {user_id})")
                
                cursor = conn.execute(update_query, (new_password, user_id))
                rows_affected = cursor.rowcount
                print(f"DEBUG: Rows affected: {rows_affected}")
                
                conn.commit()
                conn.close()
                
                # Update the in-memory password in user_model
                self.user_model.password = new_password
                print(f"✓ Password updated successfully for user: {username}")
                
                # Emit signal and close
                self.password_changed.emit(new_password, confirm_password)
                self.accept()
            except Exception as e:
                self.show_error(f"Error updating password: {str(e)}")
                print(f"ERROR: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("WARNING: No user_model provided, password not updated in database")
            # Emit signal anyway for testing purposes
            self.password_changed.emit(new_password, confirm_password)
            self.accept()
    
    def show_error(self, message: str):
        """Display error message"""
        self.error_label.setText(message)
        self.error_label.setVisible(True)
    
    def clear_form(self):
        """Clear all fields and errors"""
        self.input_new_password.clear()
        self.input_confirm_password.clear()
        self.error_label.setVisible(False)
        self.error_label.clear()
    
    def get_passwords(self):
        """Return the entered passwords"""
        return (self.input_new_password.text(), self.input_confirm_password.text())
