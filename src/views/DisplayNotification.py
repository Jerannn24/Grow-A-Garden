from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QColor

class DisplayNotification(QWidget):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # Style Container
        self.container = QWidget(self)
        self.container.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-radius: 10px;
            }
            QLabel { color: #333; }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        
        header = QHBoxLayout()
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #D32F2F;") 

        self.btn_close = QPushButton("×")
        self.btn_close.setFixedSize(20, 20)
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.setStyleSheet("border: none; font-weight: bold; font-size: 16px; color: #888;")
        self.btn_close.clicked.connect(self.close_animation)
        
        header.addWidget(self.lbl_title)
        header.addStretch()
        header.addWidget(self.btn_close)
        
        self.lbl_msg = QLabel(message)
        self.lbl_msg.setWordWrap(True)
        self.lbl_msg.setStyleSheet("font-size: 12px;")

        layout.addLayout(header)
        layout.addWidget(self.lbl_msg)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.container)

        self.setFixedSize(300, 120)

        self.timer_hide = QTimer(self)
        self.timer_hide.timeout.connect(self.close_animation)
        self.timer_hide.start(5000) 

    def show_animation(self):
        self.show()

    def close_animation(self):
        self.close()

    @staticmethod
    def show_notification(title, message, parent=None):
        popup = DisplayNotification(title, message, parent)
        if parent is not None:
            try:
                geo = parent.geometry()
                x = geo.x() + geo.width() - popup.width() - 20
                y = geo.y() + geo.height() - popup.height() - 20
                popup.move(x, y)
            except Exception:
                pass
        popup.show_animation()
        return popup