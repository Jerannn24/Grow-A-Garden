import sys
import os

from models.UserModel import DB_FILE_PATH
project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
                            QHBoxLayout, QLabel, QPushButton, QFrame, \
                            QGridLayout, QScrollArea, QSizePolicy, QStackedWidget, \
                            QMessageBox, QDialog # Tambahkan QDialog

from PyQt5.QtCore import Qt, QSize, QDateTime, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import sqlite3

from src.views.AddPlantForm import AddPlantForm
from src.controllers.PlantManager import PlantManager
from src.views.DisplayCommunity import DisplayCommunity # Jika Anda menggunakan ini
from src.models.Post import Post                       # Jika Anda menggunakan ini
from src.controllers.PostManager import PostManager
from src.models.UserModel import UserModel
# --- KONFIGURASI WARNA & STYLE (TETAP SAMA) ---
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

# --- SIDEBAR (Tetap sama) ---
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
        user_lbl.setObjectName('user_info_label')
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

# --- CLASS HEADER (Diintegrasikan ke HomeScreen.py) ---
# Di dalam HomeScreen.py

class AppHeader(QWidget):
    def __init__(self, title_text: str, subtitle_text: str = None):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9FA;")
        
        # Main Vertical Layout (menampung semua baris)
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(5) # Spacing vertikal yang lebih sedikit

        # 1. TOP ROW: Time/Date & Weather (Baris ini harus sejajar)
        top_h_layout = QHBoxLayout()
        top_h_layout.setSpacing(20) # Spacing antara waktu dan cuaca
        
        # A. Time/Date Column
        time_col = QVBoxLayout()
        time_col.setContentsMargins(0, 0, 0, 0)
        time_col.setSpacing(2)
        
        date_lbl = QLabel(QDateTime.currentDateTime().toString("dddd, MMMM dd, yyyy"))
        date_lbl.setStyleSheet("color: gray; font-size: 14px;")
        # Menggunakan waktu hardcoded dari gambar Anda untuk konsistensi visual
        time_lbl = QLabel("07:44:14 PM") 
        time_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #007F00;")
        
        time_col.addWidget(date_lbl)
        time_col.addWidget(time_lbl)
        
        top_h_layout.addLayout(time_col)
        top_h_layout.addStretch() # Pendorong
        
        # B. Weather Widget (Diletakkan di kanan, sejajar dengan waktu)
        weather_frame = QFrame()
        weather_frame.setObjectName("WeatherWidget")
        weather_frame.setFixedSize(120, 40) # Ukuran yang lebih kecil
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

        # 2. MIDDLE ROW: Title & Subtitle (Langsung di bawah waktu)
        title_v_layout = QVBoxLayout()
        title_v_layout.setContentsMargins(0, 5, 0, 0) # Mengurangi margin bawah
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

# --- CLASS PLANT CARD (Diintegrasikan ke HomeScreen.py) ---
class PlantCard(QFrame):
    def __init__(self, name, sci_name, stats, action_text=None, warning=None):
        super().__init__()
        self.setProperty("class", "plant-card")
        self.setStyleSheet("background-color: white; border-radius: 12px;")
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

# --- CLASS ADD PLANT CARD (Diintegrasikan ke HomeScreen.py) ---
class AddPlantCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("AddCard")
        self.setFixedSize(280, 320)
        self.setCursor(Qt.PointingHandCursor) # Ubah kursor jadi tangan agar terlihat bisa diklik
        
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

# --- HOME PAGE CONTENT (Dikembalikan ke content semula) ---
print("DEBUG IMPORT: Lokasi PlantManager ->", PlantManager)
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        
        # --- 1. Inisialisasi Manager ---
        self.plant_manager = PlantManager()
        # Pastikan ada user ID dummy atau dari login
        self.current_user_id = None
        # Load data awal dari DB ke memory
        self.plant_manager.loadUserData(self.current_user_id) 

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(10)
        
        # Header
        self.main_layout.addWidget(AppHeader("My Garden", "Monitor and manage your plants' health"))
        
        # --- 2. Area Scroll & Grid ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        self.content_widget = QWidget()
        self.grid = QGridLayout(self.content_widget)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        max_cols = 3 
        for i in range(max_cols): 
            self.grid.setColumnStretch(i, 1)
        
        self.scroll.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll)

        # --- 3. Render Awal ---
        self.refresh_plant_list()

    def refresh_plant_list(self):
        """Menghapus kartu lama dan menggambar ulang berdasarkan data terbaru."""
        print("--- DEBUG REFRESH ---")
        print(f"ID Objek PlantManager: {id(self.plant_manager)}")
        print(f"Isi plantList: {self.plant_manager.plantList}")
        
        if not self.current_user_id:
            print("Peringatan: UserID belum diset. Tidak memuat tanaman.")
            return
        
        # 1. HAPUS SEMUA WIDGET LAMA DARI GRID
        # Kita loop terbalik untuk menghapus dengan aman
        for i in reversed(range(self.grid.count())): 
            widget = self.grid.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None) # Lepaskan dari layout
                widget.deleteLater()   # Hapus dari memori

        # 2. TAMBAHKAN KARTU 'ADD PLANT' (Selalu di posisi Baris 0, Kolom 0)
        add_card = AddPlantCard()
        add_card.clicked.connect(self.open_add_plant_form)
        self.grid.addWidget(add_card, 0, 0)

        # 3. AMBIL DATA DARI MANAGER
        # Pastikan PlantManager punya atribut plantList yang berisi Objek Plant
        plants = self.plant_manager.plantList 

        print(f"Debug: Menampilkan {len(plants)} tanaman.") # Cek di terminal

        # 4. LOOPING UNTUK MENAMPILKAN KARTU TANAMAN
        row = 0
        col = 1 # Mulai dari kolom 1 karena kolom 0 sudah dipakai AddCard
        max_cols = 3 # Misal 3 kolom per baris (sesuaikan lebar layar)

        for plant in plants:
            # Ambil data dari OBJEK Plant (gunakan Getter)
            # Pastikan objek plant punya metode ini
            p_name = plant.getPlantName()
            p_species = plant.getPlantSpecies()
            p_media = plant.getPlantMedia()
            p_sun = plant.getLightingDuration() # Atau plant.getSunlight() jika ada

            # Siapkan data stats untuk kartu
            stats = {"🌱": p_media, "☀️": p_sun}

            # Buat Kartu
            card = PlantCard(
                name=p_name,
                sci_name=p_species,
                stats=stats,
                action_text="Details" 
            )
            
            # Masukkan ke Grid
            self.grid.addWidget(card, row, col)

            # 5. HITUNG POSISI BERIKUTNYA
            col += 1
            if col >= max_cols:
                col = 0      # Reset ke kolom pertama
                row += 1     # Pindah ke baris baru
            
            # PENTING: Jika baris baru dimulai (row > 0),
            # jangan biarkan AddCard tertimpa jika kita kembali ke (0,0).
            # Tapi logika di atas (0,0) hanya untuk AddCard. 
            # Jika row > 0, col 0 aman digunakan untuk tanaman.
            # Jika row == 0, col 0 JANGAN digunakan (skip ke 1).
            
            if row == 0 and col == 0:
                col = 1
                
    def set_current_user_id(self, userID: int):
        if self.current_user_id != userID:
            self.current_user_id = userID
            # Muat data saat UserID sudah valid
            self.plant_manager.loadUserData(self.current_user_id)
            self.refresh_plant_list()
    
    def open_add_plant_form(self):
        """Membuka dialog tambah tanaman."""
        if not self.current_user_id:
             QMessageBox.critical(self, "Error", "UserID belum terdeteksi. Silakan login ulang.")
             return
         
        form = AddPlantForm(self)
        
        if form.exec_() == QDialog.Accepted:
            # 1. Ambil data dictionary dari form
            data = form.get_data()
            
            # 2. Lengkapi data yang kurang (PENTING UNTUK CONTROLLER)
            # Controller butuh userID dan plantID untuk membuat Objek
            data['userID'] = self.current_user_id
            
            # Generate ID Sederhana (atau biarkan Controller handle UUID)
            # Agar tidak error di constructor Plant
            import time
            data['plantID'] = f"P{int(time.time())}" 
            data['date'] = "2025-01-01" # Default date string jika form tidak kirim
            
            print("Debug: Mengirim data ke Manager:", data)

            # 3. Panggil Controller
            # Pastikan di PlantManager.py nama metodenya benar (onAddClick atau addNewPlant)
            self.plant_manager.onAddClick(data) 
            
            # 4. Refresh UI
            self.refresh_plant_list()
            
            QMessageBox.information(self, "Success", f"Tanaman '{data['name']}' berhasil ditambahkan!")

# --- MAIN WINDOW (Logika Navigasi) ---
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
        
        # Inisialisasi Halaman
        self.home_page = HomePage()
        self.community_page = DisplayCommunity(db_path=DB_FILE_PATH) 
        self.todo_page = QWidget() 
        self.settings_page = QWidget() 

        self.setStyleSheet(STYLE_SHEET)
        # Tambahkan ke Stacked Widget
        self.pages.addWidget(self.home_page)      # index 0 (Home)
        self.pages.addWidget(self.community_page) # index 1 (Community)
        self.pages.addWidget(self.todo_page)      # index 2 (Todo)
        self.pages.addWidget(self.settings_page)  # index 3 (Settings)

        self.nav_buttons = self.sidebar.get_nav_buttons()
        self.nav_mapping = {
            self.nav_buttons["home"]: 0,
            self.nav_buttons["community"]: 1,
            self.nav_buttons["todo"]: 2,
            self.nav_buttons["settings"]: 3,
        }
        
        for btn, index in self.nav_mapping.items():
            btn.clicked.connect(lambda checked, i=index, b=btn: self._switch_page_and_update_sidebar(i, b))

        # Set Halaman Awal ke Home
        self.pages.setCurrentIndex(0)
        self.nav_buttons["home"].setChecked(True) 
        self.current_user = None
    
    def set_current_user(self, user_model):
        self.current_user = user_model
        
        user_lbl = self.sidebar.findChild(QLabel, 'user_info_label') 
        if user_lbl:
            user_lbl.setText(f"👤 {user_model.username}\nID: {user_model.userID}")
            
        self.home_page.set_current_user_id(user_model.userID)
        
    def _switch_page_and_update_sidebar(self, index: int, active_button: QPushButton):
        self.pages.setCurrentIndex(index)
        
        for btn in self.nav_buttons.values():
            if btn is active_button:
                btn.setChecked(True)
            else:
                btn.setChecked(False)
        
        # Panggil reload_list jika Community yang aktif
        if index == 1 and hasattr(self.community_page, 'post_manager') and hasattr(self.community_page.post_manager, 'reload_list'):
             self.community_page.post_manager.reload_list()


if __name__ == "__main__":
    # Setup DB Awal
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        Post.create_table(conn)
        conn.close()
    except Exception as e:
        print(f"Error initializing database table: {e}")

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET) 
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())