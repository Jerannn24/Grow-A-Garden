import sys
import os
project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
                            QHBoxLayout, QLabel, QPushButton, QFrame, \
                            QGridLayout, QScrollArea, QSizePolicy, QStackedWidget, \
                            QMessageBox, QDialog 

from PyQt5.QtCore import Qt, QSize, QDateTime, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import sqlite3

from src.views.AddPlantForm import AddPlantForm
from src.controllers.PlantManager import PlantManager
from src.views.DisplayCommunity import DisplayCommunity 
from src.models.Post import Post                       
from src.controllers.PostManager import PostManager

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
    
    /* Main Content Styling */
    QLabel#SectionTitle { font-size: 22px; font-weight: bold; color: #004d00; }
    QLabel#SubTitle { font-size: 12px; color: gray; }
    
    /* Plant Cards */
    QFrame.plant-card { background-color: white; border-radius: 12px; border: 1px solid #E0E0E0; }
    QFrame#WeatherWidget { background-color: #F8F9FA; border-radius: 10px; border: 1px solid #E0E0E0; }
    QFrame#AddCard { background-color: #F5F5F5; border: 2px dashed #BDBDBD; border-radius: 12px; }
"""

# SIDEBAR 
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

class AppHeader(QWidget):
    def __init__(self, title_text: str, subtitle_text: str = None):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9FA;")
        
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(5) 

        top_h_layout = QHBoxLayout()
        top_h_layout.setSpacing(20) 
        
        # Time/Date 
        time_col = QVBoxLayout()
        time_col.setContentsMargins(0, 0, 0, 0)
        time_col.setSpacing(2)
        
        date_lbl = QLabel(QDateTime.currentDateTime().toString("dddd, MMMM dd, yyyy"))
        date_lbl.setStyleSheet("color: gray; font-size: 14px;")
        
        time_lbl = QLabel("07:44:14 PM") 
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

# Plant Card
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

class AddPlantCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("AddCard")
        self.setFixedSize(280, 320)
        self.setCursor(Qt.PointingHandCursor) 
        
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

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.plant_manager = PlantManager()
        
        # ID Dummy
        self.current_user_id = "user123" 

        self.plant_manager.loadUserData(self.current_user_id) 

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(10)
        
        self.main_layout.addWidget(AppHeader("My Garden", "Monitor and manage your plants' health"))
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        self.content_widget = QWidget()
        self.grid = QGridLayout(self.content_widget)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.scroll.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll)

        self.refresh_plant_list()

    def refresh_plant_list(self):
        """Menghapus kartu lama dan menggambar ulang berdasarkan data terbaru."""
        print("--- DEBUG REFRESH ---")
        print(f"ID Objek PlantManager: {id(self.plant_manager)}")
        print(f"Isi plantList: {self.plant_manager.plantList}")
        
        for i in reversed(range(self.grid.count())): 
            widget = self.grid.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None) 
                widget.deleteLater()   

        add_card = AddPlantCard()
        add_card.clicked.connect(self.open_add_plant_form)
        self.grid.addWidget(add_card, 0, 0)

        # Ambil Data dari manager
        plants = self.plant_manager.plantList 

        print(f"Debug: Menampilkan {len(plants)} tanaman.") 

        # Loop buat nampilin tanaman
        row = 0
        col = 1 # Col 1 karena col 0 buat add plant
        max_cols = 3 

        for plant in plants:
            p_name = plant.getPlantName()
            p_species = plant.getPlantSpecies()
            p_media = plant.getPlantMedia()
            p_sun = "Sun" 

            stats = {"🌱": p_media, "☀️": p_sun}
            
            card = PlantCard(
                name=p_name,
                sci_name=p_species,
                stats=stats,
                action_text="Details" 
            )
            
            self.grid.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0      
                row += 1     
            
            if row == 0 and col == 0:
                col = 1

    def open_add_plant_form(self):
        """Membuka dialog tambah tanaman."""
        form = AddPlantForm(self)
        
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            
            data['userID'] = self.current_user_id
            import time
            data['plantID'] = f"P{int(time.time())}" 
            data['date'] = "2025-01-01" 
            
            print("Debug: Mengirim data ke Manager:", data)

            self.plant_manager.onAddClick(data) 
            self.refresh_plant_list()
            
            QMessageBox.information(self, "Success", f"Tanaman '{data['name']}' berhasil ditambahkan!")

# Main Window
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
        
        # inisiasi halaman home
        self.home_page = HomePage()
        self.community_page = DisplayCommunity(db_path="app.db") 
        self.todo_page = QWidget() 
        self.settings_page = QWidget() 

        self.pages.addWidget(self.home_page)      # indeks 0 
        self.pages.addWidget(self.community_page) # indeks 1 
        self.pages.addWidget(self.todo_page)      # indeks 2 
        self.pages.addWidget(self.settings_page)  # indeks 3 

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
    try:
        conn = sqlite3.connect("app.db")
        Post.create_table(conn)
        conn.close()
    except Exception as e:
        print(f"Error initializing database table: {e}")

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET) 
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())