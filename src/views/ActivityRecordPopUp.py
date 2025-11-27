from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor


class ActivityRecordPopUp(QDialog):
    """Popup dialog for recording actual task quantity completed"""
    
    # Signals
    confirmed = pyqtSignal(float)  # Emits the actual quantity when confirmed
    
    def __init__(self, task=None, parent=None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle("Record Activity")
        self.setModal(True)
        self.setFixedWidth(400)
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel#Title { font-size: 18px; font-weight: bold; color: #212121; }
            QLabel#Description { font-size: 14px; color: #666; }
            QLabel#Label { font-size: 12px; color: #333; font-weight: bold; }
            QLineEdit { border: 1px solid #DDD; border-radius: 6px; padding: 8px; font-size: 14px; }
            QSpinBox, QDoubleSpinBox { border: 1px solid #DDD; border-radius: 6px; padding: 8px; font-size: 14px; }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Task Title
        if self.task:
            title = QLabel(self.task.actionType.capitalize())
            title.setObjectName("Title")
            main_layout.addWidget(title)
        
        # Description
        if self.task:
            desc = QLabel(f"Complete your {self.task.actionType} task")
            desc.setObjectName("Description")
            desc.setWordWrap(True)
            main_layout.addWidget(desc)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #EEE;")
        main_layout.addWidget(separator)
        
        # Recommended Quantity Section
        if self.task:
            rec_label = QLabel("Recommended Quantity:")
            rec_label.setObjectName("Label")
            main_layout.addWidget(rec_label)
            
            # Get recommended quantity from task
            rec_quantity = self.task.quantity if hasattr(self.task, 'quantity') and self.task.quantity else 1
            rec_text = QLabel(f"Suggested: {rec_quantity} units")
            rec_text.setStyleSheet("color: #2E7D32; font-size: 13px; font-weight: bold;")
            main_layout.addWidget(rec_text)
        
        # Actual Quantity Input
        input_label = QLabel("Actual Quantity Completed:")
        input_label.setObjectName("Label")
        main_layout.addWidget(input_label)
        
        self.input_field = QSpinBox()
        self.input_field.setMinimum(0)
        self.input_field.setMaximum(1000)
        self.input_field.setValue(1)
        self.input_field.setSingleStep(1)
        main_layout.addWidget(self.input_field)
        
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
        
        self.btn_confirm = QPushButton("Confirm")
        self.btn_confirm.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_confirm.setFixedHeight(40)
        self.btn_confirm.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1B5E20;
            }
        """)
        self.btn_confirm.clicked.connect(self.confirm_action)
        
        button_layout.addWidget(self.btn_cancel, 1)
        button_layout.addWidget(self.btn_confirm, 1)
        
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def confirm_action(self):
        """Emit the confirmed signal and close the dialog"""
        actual_quantity = float(self.input_field.value())
        self.confirmed.emit(actual_quantity)
        self.accept()
    
    def get_quantity(self):
        """Return the entered quantity (for non-signal usage)"""
        return float(self.input_field.value())
