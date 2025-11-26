import sqlite3
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from models.UserModel import DB_FILE_PATH
from models.Post import Post
from views.DisplayCommunity import DisplayCommunity
from .Sidebar import Sidebar
from .HomePage import HomePage

try:
    from views.AdminReportDisplay import AdminReportDisplay
    from models.Report import Report
except ImportError:
    AdminReportDisplay = None
    Report = None


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
        
        self.conn = None
        self._setup_db()
        
        # inisiasi halaman home
        self.home_page = HomePage()
        self.community_page = DisplayCommunity(db_path=DB_FILE_PATH) 
        self.todo_page = QWidget() 
        self.settings_page = QWidget()
        
        self.reports_page = None

        self.setStyleSheet(STYLE_SHEET)
        # Tambahkan ke Stacked Widget
        self.pages.addWidget(self.home_page)      # index 0 (Home)
        self.pages.addWidget(self.community_page) # index 1 (Community)
        self.pages.addWidget(self.todo_page)      # index 2 (Todo)
        self.pages.addWidget(self.settings_page)  # index 3 (Settings)

        # Placeholder for reports page so navigation index stays stable
        self._reports_placeholder = QWidget()
        self._reports_placeholder.setVisible(False)
        self.pages.addWidget(self._reports_placeholder)  # index 4 (placeholder)

        self.nav_buttons = self.sidebar.get_nav_buttons()
        self.nav_mapping = {
            self.nav_buttons["home"]: 0,
            self.nav_buttons["community"]: 1,
            self.nav_buttons["todo"]: 2,
            self.nav_buttons["settings"]: 3,
        }
        if "reports" in self.nav_buttons:
            # Report index 4
            self.nav_mapping[self.nav_buttons["reports"]] = 4
        
        for btn, index in self.nav_mapping.items():
            btn.clicked.connect(lambda checked, i=index, b=btn: self._switch_page_and_update_sidebar(i, b))

        self.pages.setCurrentIndex(0)
        self.nav_buttons["home"].setChecked(True) 
        self.current_user = None
    
    def _setup_db(self):
        """Setup database connection."""
        try:
            self.conn = sqlite3.connect(DB_FILE_PATH)
            self.conn.row_factory = sqlite3.Row
            if Report:
                Report.create_table(self.conn)
        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            self.conn = None
    
    def set_current_user(self, user_model):
        self.current_user = user_model
        
        user_lbl = self.sidebar.findChild(QLabel, 'user_info_label')
        if user_lbl:
            user_lbl.setText(f"👤 {user_model.username}\nID: {user_model.userID}")
            
        self.home_page.set_current_user_id(user_model.userID)
        
        # Set current user in community page's post manager
        if hasattr(self.community_page, 'post_manager'):
            self.community_page.post_manager.set_current_user(user_model)
        
        is_admin = user_model.role == "admin"
        self.sidebar.set_admin_mode(is_admin)
        
        if is_admin:
            if self.reports_page is None and AdminReportDisplay and self.conn:
                self.reports_page = AdminReportDisplay(DB_FILE_PATH, self.conn, user_model, self)
                try:

                    placeholder = self._reports_placeholder
                    self.pages.removeWidget(placeholder)
                except Exception:
                    pass
                self.pages.insertWidget(4, self.reports_page)

                if "reports" in self.nav_buttons:
                    self.nav_mapping[self.nav_buttons["reports"]] = 4
                    self.nav_buttons["reports"].clicked.connect(
                        lambda checked, i=4, b=self.nav_buttons["reports"]: 
                        self._switch_page_and_update_sidebar(i, b)
                    )
        
    def _switch_page_and_update_sidebar(self, index: int, active_button: QPushButton):
        self.pages.setCurrentIndex(index)
        
        for btn in self.nav_buttons.values():
            if btn is active_button:
                btn.setChecked(True)
            else:
                btn.setChecked(False)
        
        if index == 1 and hasattr(self.community_page, 'post_manager') and hasattr(self.community_page.post_manager, 'reload_list'):
             self.community_page.post_manager.reload_list()
