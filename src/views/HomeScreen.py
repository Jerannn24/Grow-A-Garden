import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, 
                             QGridLayout, QScrollArea, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QIcon

# --- KONFIGURASI WARNA & STYLE ---
STYLE_SHEET = """
    QMainWindow {
        background-color: #F8F9FA;
    }
    /* Sidebar Styling */
    QFrame#Sidebar {
        background-color: #007F00; /* Warna Hijau Dominan */
        border: none;
    }
    QLabel#AppTitle {
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 20px;
    }
    QPushButton.nav-btn {
        background-color: transparent;
        color: white;
        text-align: left;
        padding: 12px 20px;
        border: none;
        font-size: 14px;
        border-radius: 8px;
    }
    QPushButton.nav-btn:hover {
        background-color: #006600;
    }
    QPushButton.nav-btn:checked {
        background-color: white;
        color: #007F00;
        font-weight: bold;
    }
    
    /* Main Content Styling */
    QLabel#SectionTitle {
        font-size: 22px;
        font-weight: bold;
        color: #004d00;
    }
    QLabel#SubTitle {
        font-size: 12px;
        color: gray;
    }
    
    /* Weather Widget */
    QFrame#WeatherWidget {
        background-color: #FFF8E1; /* Kuning pucat */
        border-radius: 15px;
    }

    /* Plant Cards */
    QFrame.plant-card {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
    }
    QFrame#ImagePlaceholder {
        background-color: #EEEEEE;
        border-radius: 8px;
    }
    QPushButton#ActionBtn {
        background-color: #E3F2FD;
        color: #1976D2;
        border: none;
        border-radius: 6px;
        padding: 8px;
        font-weight: bold;
    }
    QLabel#StatusWarning {
        background-color: #FFF9C4;
        color: #FBC02D;
        padding: 5px;
        border-radius: 5px;
        font-size: 11px;
    }

    /* Add Card */
    QFrame#AddCard {
        background-color: #F5F5F5;
        border: 2px dashed #BDBDBD;
        border-radius: 12px;
    }
"""

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(250)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Grow a Garden")
        title.setObjectName("AppTitle")
        layout.addWidget(title)
        
        layout.addSpacing(20)

        # Navigation Buttons
        self.btn_home = self.create_nav_btn("🏠  Home", active=True)
        self.btn_comm = self.create_nav_btn("👥  Community")
        self.btn_todo = self.create_nav_btn("✅  Todo List")
        
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_comm)
        layout.addWidget(self.btn_todo)
        
        # Spacer to push settings to bottom
        layout.addStretch()
        
        # Bottom Settings
        self.btn_settings = self.create_nav_btn("⚙️  Settings")
        layout.addWidget(self.btn_settings)
        
        # User Profile Dummy
        user_lbl = QLabel("👤  John Doe\n      Profile")
        user_lbl.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(user_lbl)
        
        self.setLayout(layout)

    def create_nav_btn(self, text, active=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(active)

        btn.setProperty("class", "nav-btn") 

        btn.setStyleSheet("""
            QPushButton { text-align: left; padding: 12px; border-radius: 8px; color: white; background: transparent; font-size: 14px;}
            QPushButton:hover { background-color: rgba(255,255,255,0.2); }
            QPushButton:checked { background-color: white; color: #007F00; font-weight: bold; }
        """)
        return btn

class PlantCard(QFrame):
    def __init__(self, name, sci_name, stats, action_text=None, warning=None):
        super().__init__()
        self.setProperty("class", "plant-card") # For QSS targeting if using generic approach
        self.setStyleSheet("background-color: white; border-radius: 12px; border: 1px solid #E0E0E0;")
        self.setFixedSize(280, 320)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Plant Image Placeholder
        img_placeholder = QLabel("🌿")
        img_placeholder.setAlignment(Qt.AlignCenter)
        img_placeholder.setStyleSheet("background-color: #EEEEEE; border-radius: 8px; font-size: 40px;")
        img_placeholder.setFixedHeight(120)
        layout.addWidget(img_placeholder)
        
        # Title & Subtitle
        title_lbl = QLabel(name)
        title_lbl.setStyleSheet("font-weight: bold; font-size: 16px;")
        sub_lbl = QLabel(sci_name)
        sub_lbl.setStyleSheet("color: gray; font-size: 12px; font-style: italic;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(sub_lbl)
        
        # Stats (Water / Sun)
        stats_layout = QHBoxLayout()
        for icon, val in stats.items():
            lbl = QLabel(f"{icon} {val}")
            lbl.setStyleSheet("color: #555; background: #F5F5F5; padding: 4px 8px; border-radius: 4px;")
            stats_layout.addWidget(lbl)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        layout.addStretch()
        
        # Action Button or Warning
        if warning:
            warn_lbl = QLabel(warning)
            warn_lbl.setAlignment(Qt.AlignCenter)
            warn_lbl.setStyleSheet("background-color: #FFF9C4; color: #FBC02D; padding: 8px; border-radius: 6px; font-weight: bold;")
            layout.addWidget(warn_lbl)
        elif action_text:
            btn = QPushButton(action_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("background-color: #E3F2FD; color: #1976D2; border: none; border-radius: 6px; padding: 10px; font-weight: bold;")
            layout.addWidget(btn)
            
        self.setLayout(layout)

class AddPlantCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("AddCard")
        self.setFixedSize(280, 320)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel("➕")
        icon.setStyleSheet("font-size: 40px; color: gray;")
        icon.setAlignment(Qt.AlignCenter)
        
        text = QLabel("Add Plant")
        text.setStyleSheet("color: gray; font-weight: bold; margin-top: 10px;")
        text.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(text)
        self.setLayout(layout)

class Header(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Date Time Area
        date_layout = QVBoxLayout()
        date_lbl = QLabel("Wednesday, November 12, 2025")
        date_lbl.setStyleSheet("color: gray;")
        time_lbl = QLabel("07:44:14 PM")
        time_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #007F00;")
        
        date_layout.addWidget(date_lbl)
        date_layout.addWidget(time_lbl)
        
        layout.addLayout(date_layout)
        layout.addStretch()
        
        # Weather Widget
        weather_frame = QFrame()
        weather_frame.setObjectName("WeatherWidget")
        weather_frame.setFixedSize(250, 60)
        w_layout = QHBoxLayout(weather_frame)
        
        w_icon = QLabel("☀️")
        w_icon.setStyleSheet("font-size: 24px;")
        w_info = QLabel("<b>28°C</b><br>Sunny")
        w_loc = QLabel("📍 Jakarta, Indonesia")
        w_loc.setStyleSheet("font-size: 10px; color: gray;")
        
        w_layout.addWidget(w_icon)
        w_layout.addWidget(w_info)
        w_layout.addWidget(w_loc)
        
        layout.addWidget(weather_frame)
        self.setLayout(layout)

class MainContent(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 1. Header
        layout.addWidget(Header())
        
        layout.addSpacing(10)
        
        # 2. Section Title
        title = QLabel("My Garden")
        title.setObjectName("SectionTitle")
        subtitle = QLabel("Monitor and manage your plants' health")
        subtitle.setObjectName("SubTitle")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        # 3. Scroll Area for Cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        grid = QGridLayout(content_widget)
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        # -- ADD CARDS --
        # Card 0: Add Plant
        grid.addWidget(AddPlantCard(), 0, 0)
        
        # Card 1: Monstera
        c1 = PlantCard("Monstera Deliciosa", "Monstera deliciosa", 
                       {"💧": "60%", "☀️": "50%"}, action_text="Water today")
        grid.addWidget(c1, 0, 1)
        
        # Card 2: Pothos (Warning)
        c2 = PlantCard("Golden Pothos", "Epipremnum aureum", 
                       {"💧": "40%", "☀️": "30%"}, warning="Needs sunlight")
        grid.addWidget(c2, 0, 2)
        
        # Card 3: Cactus (Dummy)
        c3 = PlantCard("Cactus", "Cactaceae", {"💧": "10%", "☀️": "90%"}, action_text="Water in 5 days")
        grid.addWidget(c3, 1, 0)

        # Card 4: Sunflower (Dummy)
        c4 = PlantCard("Sunflower", "Helianthus", {"💧": "80%", "☀️": "100%"}, action_text="Water today")
        grid.addWidget(c4, 1, 1)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grow a Garden UI")
        self.resize(1200, 800)
        
        # Main Layout (Split Screen)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Add Main Content
        self.content = MainContent()
        main_layout.addWidget(self.content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET) # Apply Global Styles
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())