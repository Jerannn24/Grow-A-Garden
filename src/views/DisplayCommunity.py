import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QDateTime
from src.controllers.PostManager import PostManager

# --- 1. MULTI-WIDGET HEADER (Sesuai Gambar I-08) ---
class CommunityHeader(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9FA;")
        
        main_h_layout = QHBoxLayout(self)
        main_h_layout.setContentsMargins(0, 0, 0, 0) 
        main_h_layout.setSpacing(10)

        # A. TIME COLUMN (Kiri)
        time_col = QVBoxLayout()
        time_col.setContentsMargins(0, 0, 0, 0)
        time_col.setSpacing(2)

        # Tanggal (Wednesday, Wednesday, November 12, 2025)
        date_lbl = QLabel("Wednesday, Wednesday, November 12, 2025")
        date_lbl.setStyleSheet("color: gray; font-size: 14px;")
        
        # Waktu Besar dan Tebal
        time_lbl = QLabel("09:27:35 PM") 
        time_lbl.setStyleSheet("font-size: 30px; font-weight: bold; color: #007F00;")
        
        time_col.addWidget(date_lbl)
        time_col.addWidget(time_lbl)

        main_h_layout.addLayout(time_col)
        main_h_layout.addStretch()

        # B. WEATHER & INFO WIDGETS (Kanan - Menggunakan QFrame tunggal untuk setiap kotak)
        
        def create_info_box(icon, main_text, sub_text=None, location=None):
            frame = QFrame()
            frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 5px 10px; border: 1px solid #ddd;")
            v_layout = QVBoxLayout(frame)
            v_layout.setContentsMargins(5, 5, 5, 5)
            v_layout.setSpacing(2)
            
            # Baris Utama (Icon + Main Text)
            h_top_layout = QHBoxLayout()
            h_top_layout.setContentsMargins(0, 0, 0, 0)
            
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet("font-size: 16px;")
            
            main_lbl = QLabel(f"<b>{main_text}</b>")
            main_lbl.setStyleSheet("font-size: 14px; margin-left: 5px;")
            
            h_top_layout.addWidget(icon_lbl)
            h_top_layout.addWidget(main_lbl)
            h_top_layout.addStretch()
            
            v_layout.addLayout(h_top_layout)

            # Sub Text (Sunny/Humidity)
            if sub_text:
                sub_lbl = QLabel(sub_text)
                sub_lbl.setStyleSheet("color: gray; font-size: 11px; margin-left: 18px;")
                v_layout.addWidget(sub_lbl)
            
            # Lokasi
            if location:
                loc_lbl = QLabel(location)
                loc_lbl.setStyleSheet("color: #795548; font-size: 11px; margin-left: 18px;")
                v_layout.addWidget(loc_lbl)

            return frame

        # Kotak 1: Suhu & Cuaca
        main_h_layout.addWidget(create_info_box("☀️", "28°C", "Sunny"))
        
        # Kotak 2: Angin & Kelembaban
        main_h_layout.addWidget(create_info_box("💨", "12 km/h", "Humidity: 65%"))

        # Kotak 3: Lokasi (di gambar I-08, ini adalah kotak info terpisah)
        main_h_layout.addWidget(create_info_box("📍", "Jakarta, Indonesia"))


# --- 2. SHARE POST WIDGET (Input Post Baru - Mematuhi tata letak Gambar I-08) ---
class SharePostWidget(QWidget):
    def __init__(self, post_manager, parent=None):
        super().__init__(parent)
        self.post_manager = post_manager
        
        # Menggunakan QFrame sebagai container untuk styling background putih
        frame = QFrame()
        # Mengurangi padding untuk membuat box lebih kecil
        frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px; border: 1px solid #E0E0E0;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(frame)

        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(15, 15, 15, 15)
        
        # 1. Input Row
        input_row = QHBoxLayout()
        input_row.setSpacing(10)
        
        # Avatar Placeholder (Kiri)
        avatar_lbl = QLabel("🌱")
        avatar_lbl.setFixedSize(30, 30)
        avatar_lbl.setAlignment(Qt.AlignCenter)
        avatar_lbl.setStyleSheet("background-color: #E8F5E9; border-radius: 15px; font-size: 16px;")
        
        # Input Text (Placeholder)
        self.input_label = QLabel("Share your gardening moment...")
        self.input_label.setCursor(Qt.PointingHandCursor)
        self.input_label.setStyleSheet("font-size: 14px; color: gray; border: none; padding-left: 10px;")
        
        input_row.addWidget(avatar_lbl)
        input_row.addWidget(self.input_label)
        input_row.addStretch()
        
        frame_layout.addLayout(input_row)

        # 2. Action Row (Icons)
        actions_row = QHBoxLayout()
        # Mengatur margin lebih kecil karena tombol Post dihapus
        actions_row.setContentsMargins(40, 5, 0, 0) 
        actions_row.setSpacing(10)
        
        # Ikon Media (Gambar) - Diganti menjadi tombol yang memicu pop-up
        self.btn_media = QPushButton("🖼️") 
        self.btn_media.setStyleSheet("background: none; border: none; font-size: 18px; color: #007F00;")
        self.btn_media.clicked.connect(self._open_create_post) 

        # Ikon Like (Dummy)
        like_icon = QLabel("🤍") 
        
        actions_row.addWidget(self.btn_media)
        actions_row.addWidget(like_icon)
        actions_row.addStretch()
        
        # Tombol POST (dihapus dari sini karena duplikasi, hanya ada di pop-up)
        # Jika Anda ingin tombol Post tampil di sini (seperti gambar I-08):
        self.post_button = QPushButton("Post")
        self.post_button.setFixedSize(70, 30)
        self.post_button.setStyleSheet("""
            QPushButton {
                background-color: #8BC34A;
                color: white; 
                border-radius: 15px; 
                font-weight: bold;
            }
        """)
        self.post_button.clicked.connect(self._open_create_post)
        actions_row.addWidget(self.post_button)
        
        frame_layout.addLayout(actions_row)

        # Connections (Input label tetap memicu dialog create post)
        self.input_label.mousePressEvent = lambda event: self._open_create_post()

    def _open_create_post(self):
        # ... (Logika yang sama) ...
        if hasattr(self.post_manager, 'switch_to_create_post'):
            self.post_manager.switch_to_create_post()


# --- 3. COMMUNITY PAGE (Menyatukan semua komponen) ---
class DisplayCommunity(QWidget):
    def __init__(self, db_path: str = "app.db", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        # Margin yang sesuai agar konten tidak mepet tepi
        layout.setContentsMargins(30, 30, 30, 30) 
        layout.setSpacing(20) # Spacing antar widget

        # 1. Multi-Widget Header (Waktu, Cuaca, dll.)
        header_widget = CommunityHeader()
        layout.addWidget(header_widget) 

        # 2. Judul Utama Community Feed & Slogan
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)

        title_lbl = QLabel("Community Feed")
        title_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-top: 15px;")
        
        slogan_lbl = QLabel("Share your gardening journey")
        slogan_lbl.setStyleSheet("font-size: 14px; color: gray;")
        
        title_layout.addWidget(title_lbl)
        title_layout.addWidget(slogan_lbl)
        
        layout.addWidget(title_container)
        
        # 3. Share Post Widget (Input di atas feed)
        self.post_manager = PostManager(db_path=db_path)
        share_post_widget = SharePostWidget(post_manager=self.post_manager)
        layout.addWidget(share_post_widget)
        
        # 4. Tab Navigasi (Recent, Top Likes, Top Views)
        tab_layout = QHBoxLayout()
        # Perlu menggunakan QPushButton dengan style yang sesuai
        self.btn_recent = self._create_tab_button("Recent", is_active=True)
        self.btn_likes = self._create_tab_button("Top Likes")
        self.btn_views = self._create_tab_button("Top Views")
        
        # KUNCI: Menghubungkan tombol tab ke PostManager
        self.btn_recent.clicked.connect(lambda: self.post_manager.reload_list("timeCreated"))
        self.btn_likes.clicked.connect(lambda: self.post_manager.reload_list("likes"))
        self.btn_views.clicked.connect(lambda: self.post_manager.reload_list("views"))
        
        tab_layout.addWidget(self.btn_recent)
        tab_layout.addWidget(self.btn_likes)
        tab_layout.addWidget(self.btn_views)
        tab_layout.addStretch()
        
        layout.addLayout(tab_layout)

        # 5. PostManager Content (Feed itu sendiri)
        # Asumsi: PostManager hanya menampilkan QListWidget (daftar post) dan logika kosong/ada post.
        layout.addWidget(self.post_manager)
        
        layout.addStretch()
        
    def _create_tab_button(self, text, is_active=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setChecked(is_active)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #EFEFEF; 
                border: 1px solid #DDD; 
                border-radius: 15px; 
                padding: 5px 15px;
                margin-right: 5px;
            }
            QPushButton:checked {
                background-color: #007F00; /* Warna hijau solid */
                color: white; 
                font-weight: bold;
            }
        """)
        return btn