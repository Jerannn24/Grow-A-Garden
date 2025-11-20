import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, 
                             QGridLayout, QScrollArea, QSizePolicy, QStackedWidget)
from PyQt5.QtCore import Qt, QSize, QDateTime
from PyQt5.QtGui import QFont, QColor
import sqlite3

# ============================================
# PATH CONFIGURATION - SOLUSI UTAMA
# ============================================
# Dapatkan path absolut dari file ini
THIS_FILE = os.path.abspath(__file__)  # /path/to/src/views/HomeScreen.py
VIEWS_DIR = os.path.dirname(THIS_FILE)  # /path/to/src/views
SRC_DIR = os.path.dirname(VIEWS_DIR)    # /path/to/src
PROJECT_ROOT = os.path.dirname(SRC_DIR) # /path/to/project

# Tambahkan src ke sys.path jika belum ada
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Database path - SELALU di dalam folder src
DB_PATH = os.path.join(SRC_DIR, "app.db")

# ============================================
# IMPORTS WITH ERROR HANDLING
# ============================================
try:
    from views.DisplayCommunity import DisplayCommunity
    from models.Post import Post
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"sys.path: {sys.path}")
    print(f"SRC_DIR: {SRC_DIR}")
    
    # Fallback dummy classes
    class DisplayCommunity(QWidget):
        def __init__(self, db_path, parent=None):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            error_label = QLabel(f"❌ Community View Load Failed\n\nError: {e}\n\nPastikan semua file ada di:\n{SRC_DIR}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            error_label.setWordWrap(True)
            layout.addWidget(error_label)

    class Post:
        @staticmethod
        def create_table(conn):
            return None

# --- STYLE SHEET (TETAP SAMA) ---
STYLE_SHEET = """
    QMainWindow { background-color: #F8F9FA; }
    
    QFrame#Sidebar { background-color: #007F00; border: none; }
    QLabel#AppTitle { color: white; font-size: 20px; font-weight: bold; padding: 20px; }
    
    QPushButton.nav-btn {
        background-color: transparent;
        color: white;
        text-align: left;
        padding: 12px 20px;
        border: none;
        font-size: 14px;
        border-radius: 8px;
    }
    QPushButton.nav-btn:hover { background-color: #006600; }
    
    QPushButton.nav-btn:checked { 
        background-color: white;
        color: #007F00;
        font-weight: bold;
    }
    
    QLabel#SectionTitle { font-size: 22px; font-weight: bold; color: #004d00; }
    QLabel#SubTitle { font-size: 12px; color: gray; }
    
    QFrame.plant-card { background-color: white; border-radius: 12px; border: 1px solid #E0E0E0; }
    QFrame#WeatherWidget { background-color: #F8F9FA; border-radius: 10px; border: 1px solid #E0E0E0; }
    QFrame#AddCard { background-color: #F5F5F5; border: 2px dashed #BDBDBD; border-radius: 12px; }
"""

# --- SIDEBAR ---
class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(250)
        self._buttons = {}
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        
        title = QLabel("Grow a Garden")
        title.setObjectName("AppTitle")
        layout.addWidget(title)
        layout.addSpacing(20)

        self.btn_home = self.create_nav_btn("🏠 Home", "home")
        self.btn_comm = self.create_nav_btn("👥 Community", "community")
        self.btn_todo = self.create_nav_btn("✅ Todo List", "todo")
        
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_comm)
        layout.addWidget(self.btn_todo)
        
        layout.addStretch()
        
        self.btn_settings = self.create_nav_btn("⚙️ Settings", "settings")
        layout.addWidget(self.btn_settings)
        
        user_lbl = QLabel("👤 John Doe\nProfile")
        user_lbl.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(user_lbl)
        
        self.setLayout(layout)

    def create_nav_btn(self, text, name):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setProperty("class", "nav-btn") 
        self._buttons[name] = btn 
        return btn
    
    def get_nav_buttons(self):
        return self._buttons

# --- APP HEADER ---
class AppHeader(QWidget):
    def __init__(self, title_text: str, subtitle_text: str = None):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9FA;")
        
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(5)

        # TOP ROW
        top_h_layout = QHBoxLayout()
        top_h_layout.setSpacing(20)
        
        # Time/Date Column
        time_col = QVBoxLayout()
        time_col.setContentsMargins(0, 0, 0, 0)
        time_col.setSpacing(2)
        
        date_lbl = QLabel(QDateTime.currentDateTime().toString("dddd, MMMM dd, yyyy"))
        date_lbl.setStyleSheet("color: gray; font-size: 14px;")
        time_lbl = QLabel(QDateTime.currentDateTime().toString("hh:mm:ss AP"))
        time_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #007F00;")
        
        time_col.addWidget(date_lbl)
        time_col.addWidget(time_lbl)
        
        top_h_layout.addLayout(time_col)
        top_h_layout.addStretch()
        
        # Weather Widget
        weather_frame = QFrame()
        weather_frame.setObjectName("WeatherWidget")
        weather_frame.setFixedSize(120, 40)
        w_layout = QHBoxLayout(weather_frame)
        w_layout.setContentsMargins(5, 5, 5, 5)
        
        w_icon = QLabel("☀️")
        w_icon.setStyleSheet("font-size: 20px;")
        w_info = QLabel("<b>28°C</b> Sunny")
        w_info.setStyleSheet("font-size: 14px; color: #333;")

        w_layout.addWidget(w_icon)
        w_layout.addWidget(w_info)
        w_layout.addStretch()
        
        top_h_layout.addWidget(weather_frame)
        main_v_layout.addLayout(top_h_layout)

        # TITLE ROW
        title_v_layout = QVBoxLayout()
        title_v_layout.setContentsMargins(0, 5, 0, 0)
        title_v_layout.setSpacing(2)

        title = QLabel(title_text)
        title.setObjectName("SectionTitle")
        
        if subtitle_text:
            subtitle = QLabel(subtitle_text)
            subtitle.setObjectName("SubTitle")
            title_v_layout.addWidget(title)
            title_v_layout.addWidget(subtitle)
        else:
            title_v_layout.addWidget(title)

        main_v_layout.addLayout(title_v_layout)

# --- PLANT CARD ---
class PlantCard(QFrame):
    def __init__(self, name, sci_name, stats, action_text=None, warning=None):
        super().__init__()
        self.setProperty("class", "plant-card")
        self.setStyleSheet("background-color: white; border-radius: 12px; border: 1px solid #E0E0E0;")
        self.setFixedSize(280, 320)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        img_placeholder = QLabel("🌿")
        img_placeholder.setAlignment(Qt.AlignCenter)
        img_placeholder.setStyleSheet("background-color: #EEEEEE; border-radius: 8px; font-size: 40px;")
        img_placeholder.setFixedHeight(120)
        layout.addWidget(img_placeholder)
        
        title_lbl = QLabel(name)
        title_lbl.setStyleSheet("font-weight: bold; font-size: 16px;")
        sub_lbl = QLabel(sci_name)
        sub_lbl.setStyleSheet("color: gray; font-size: 12px; font-style: italic;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(sub_lbl)
        
        stats_layout = QHBoxLayout()
        for icon, val in stats.items():
            lbl = QLabel(f"{icon} {val}")
            lbl.setStyleSheet("color: #555; background: #F5F5F5; padding: 4px 8px; border-radius: 4px;")
            stats_layout.addWidget(lbl)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        layout.addStretch()
        
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

# --- ADD PLANT CARD ---
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

# --- HOME PAGE ---
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)
        
        layout.addWidget(AppHeader("My Garden", "Monitor and manage your plants' health"))
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        grid = QGridLayout(content_widget)
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        grid.addWidget(AddPlantCard(), 0, 0)
        
        c1 = PlantCard("Monstera Deliciosa", "Monstera deliciosa", 
                        {"💧": "60%", "☀️": "50%"}, action_text="Water today")
        grid.addWidget(c1, 0, 1)
        
        c2 = PlantCard("Golden Pothos", "Epipremnum aureum", 
                        {"💧": "40%", "☀️": "30%"}, warning="Needs sunlight")
        grid.addWidget(c2, 0, 2)
        
        c3 = PlantCard("Cactus", "Cactaceae", {"💧": "10%", "☀️": "90%"}, action_text="Water in 5 days")
        grid.addWidget(c3, 1, 0)

        c4 = PlantCard("Sunflower", "Helianthus", {"💧": "80%", "☀️": "100%"}, action_text="Water today")
        grid.addWidget(c4, 1, 1)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

# --- MAIN WINDOW ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grow a Garden UI")
        self.resize(1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)
        
        # Inisialisasi Halaman dengan DB_PATH yang benar
        self.home_page = HomePage()
        self.community_page = DisplayCommunity(db_path=DB_PATH)  # <-- GUNAKAN DB_PATH
        self.todo_page = QWidget() 
        self.settings_page = QWidget() 

        self.pages.addWidget(self.home_page)      
        self.pages.addWidget(self.community_page) 
        self.pages.addWidget(self.todo_page)      
        self.pages.addWidget(self.settings_page)  

        self.nav_buttons = self.sidebar.get_nav_buttons()
        self.nav_mapping = {
            self.nav_buttons["home"]: 0,
            self.nav_buttons["community"]: 1,
            self.nav_buttons["todo"]: 2,
            self.nav_buttons["settings"]: 3,
        }
        
        for btn, index in self.nav_mapping.items():
            btn.clicked.connect(lambda checked, i=index, b=btn: self._switch_page_and_update_sidebar(i, b))

        self.pages.setCurrentIndex(0)
        self.nav_buttons["home"].setChecked(True) 

    def _switch_page_and_update_sidebar(self, index: int, active_button: QPushButton):
        self.pages.setCurrentIndex(index)
        
        for btn in self.nav_buttons.values():
            if btn is active_button:
                btn.setChecked(True)
            else:
                btn.setChecked(False)
        
        if index == 1 and hasattr(self.community_page, 'post_manager') and hasattr(self.community_page.post_manager, 'reload_list'):
             self.community_page.post_manager.reload_list()


if __name__ == "__main__":
    # Setup DB dengan path yang benar
    print(f"🗄️  Database location: {DB_PATH}")
    print(f"📁 Running from: {os.getcwd()}")
    print(f"📂 SRC_DIR: {SRC_DIR}")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        Post.create_table(conn)
        conn.close()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET) 
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())