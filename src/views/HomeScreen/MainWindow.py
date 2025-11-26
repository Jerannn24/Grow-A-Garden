import sqlite3
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from models.UserModel import DB_FILE_PATH
from models.Post import Post
from views.DisplayCommunity import DisplayCommunity
from .Sidebar import Sidebar
from .AppHeader import AppHeader
from .HomePage import HomePage
from views.PlantDetails import PlantDetails
from controllers.ToDoListManager import ToDoListManager


from models.UserModel import UserModel
from typing import Optional
from views.DisplayProfile import DisplayProfile
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


class MainWindow(QMainWindow):
    logoutRequested = pyqtSignal()
    profileUpdateRequested = pyqtSignal(str, str, str, str)
    def __init__(self):
        super().__init__()
        self.current_user: Optional[UserModel] = None
        self.setWindowTitle("Grow a Garden UI")
        self.resize(1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = Sidebar(self.current_user)
        main_layout.addWidget(self.sidebar)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.topbar = AppHeader("My Garden", "Monitor and manage your plants' health")
        right_layout.addWidget(self.topbar)
        
        self.pages = QStackedWidget()
        right_layout.addWidget(self.pages)
        
        main_layout.addWidget(right_widget)
 
        self.home_page = HomePage()
        self.community_page = DisplayCommunity(db_path=DB_FILE_PATH) 
        self.todo_page = ToDoListManager(self.current_user)
        self.settings_page = QWidget() 
        self.detail_page = PlantDetails()

        self.profile_page = DisplayProfile(self.current_user, self)
        
        self.setStyleSheet(STYLE_SHEET)
 
        self.pages.addWidget(self.home_page)      
        self.pages.addWidget(self.community_page) 
        self.pages.addWidget(self.todo_page)      
        self.pages.addWidget(self.settings_page) 
        self.pages.addWidget(self.detail_page)   
        self.pages.addWidget(self.profile_page)
        
        self.nav_buttons = self.sidebar.get_nav_buttons()
        
        self.nav_mapping = {
            self.nav_buttons["home"]: 0,
            self.nav_buttons["community"]: 1,
            self.nav_buttons["todo"]: 2,
            self.nav_buttons["settings"]: 3,
        }
        
        for btn, index in self.nav_mapping.items():
            btn.clicked.connect(lambda checked, i=index, b=btn: self._switch_page_and_update_sidebar(i, b))

        self.init_connections()
        
    def init_connections(self):
        if hasattr(self.sidebar, 'connect_profile_action'):
            self.sidebar.connect_profile_action(self.displayProfile) 
            
        self.pages.setCurrentIndex(0)
        self.nav_buttons["home"].setChecked(True) 
        self.current_user = None

        self.home_page.openDetailRequested.connect(self.show_plant_details)
        self.detail_page.backRequested.connect(self.go_back_to_home)
        
        # Connect todo page back button
        if isinstance(self.todo_page, ToDoListManager):
            self.todo_page.backRequested.connect(self.go_back_to_home)
    
        
    def displayProfile(self):       
        if self.current_user is not None:
             self.profile_page.update_user_data(self.current_user) 
             
        self.pages.setCurrentWidget(self.profile_page) 
        
        for btn in self.nav_buttons.values():
            btn.setChecked(False)
 
    def set_current_user(self, user_model):
        self.current_user = user_model
        
        if hasattr(self.sidebar, 'update_profile_button'):
            self.sidebar.update_profile_button(user_model)
            
        self.profile_page.update_user_data(user_model)
        
        user_lbl = self.sidebar.findChild(QLabel, 'user_info_label')
        if user_lbl:
            user_lbl.setText(f"👤 {user_model.username}\nID: {user_model.userID}")
            
        self.home_page.set_current_user_id(user_model.userID)
        self.home_page.refresh_plant_list()
        
        if hasattr(self.community_page, 'post_manager'):
            self.community_page.post_manager.set_current_user(user_model)
        
        # Set user for todo list manager
        if isinstance(self.todo_page, ToDoListManager):
            self.todo_page.set_current_user(user_model)
        
    def _switch_page_and_update_sidebar(self, index: int, active_button: QPushButton):
        self.pages.setCurrentIndex(index)
        
        for btn in self.nav_buttons.values():
            if btn is active_button:
                btn.setChecked(True)
            else:
                btn.setChecked(False)
        
        if index == 1 and hasattr(self.community_page, 'post_manager') and hasattr(self.community_page.post_manager, 'reload_list'):
             self.community_page.post_manager.reload_list()
        
        # Refresh todo list when switching to it
        if index == 2 and isinstance(self.todo_page, ToDoListManager):
             self.todo_page.refresh_tasks()
    
    def show_plant_details(self, plant_id):
        print(f"Navigasi ke Detail Tanaman ID: {plant_id}")
        
        target_plant = next((p for p in self.home_page.plant_manager.plantList if p.plantID == plant_id), None)
        
        if target_plant and self.current_user:
            self.detail_page.populate_data(target_plant, self.current_user.getUserID())
            self.pages.setCurrentIndex(4) 
            for btn in self.nav_buttons.values():
                btn.setChecked(False)
        else:
            if not target_plant:
                print(f"Error: Data tanaman ID {plant_id} tidak ditemukan di memory.")
            else:
                print("Error: User belum login")

    def go_back_to_home(self):
        self._switch_page_and_update_sidebar(0, self.nav_buttons["home"])