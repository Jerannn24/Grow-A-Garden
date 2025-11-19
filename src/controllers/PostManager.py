import sqlite3
import sys
import os
from typing import Optional, List, Any
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QListWidget, QListWidgetItem, QInputDialog, QApplication, QLabel, QPushButton, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon

# pastikan 'src' dan project root ada di sys.path supaya import package-style atau module-level keduanya bekerja
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_src_dir = os.path.join(_project_root, 'src')
for p in (_src_dir, _project_root):
    if p and p not in sys.path:
        sys.path.insert(0, p)

# Coba import package-qualified lalu fallback ke modul-level import
try:
    from src.views.DisplayPost import DisplayPost
except Exception:
    # Asumsi DisplayPost.py sudah tersedia di folder yang sama untuk uji coba
    try:
        from views.DisplayPost import DisplayPost
    except ImportError:
        # Jika DisplayPost tidak ada, buat dummy class untuk kompilasi
        class DisplayPost(QWidget):
            def render_post(self, post, replies_count=0):
                self.setLayout(QVBoxLayout())
                self.layout().addWidget(QLabel(f"Detail Post ID {post.getPostID()}"))


try:
    from src.models.Post import Post
except Exception:
    from models.Post import Post

# --- NEW: CreatePostWidget Class (untuk input post baru) ---
class CreatePostWidget(QWidget):
    def __init__(self, post_manager, parent=None):
        super().__init__(parent)
        self.post_manager = post_manager
        self.selected_media_path: str = "" # Variable untuk menyimpan path gambar sementara
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # ... (Title dan Input Title tetap sama) ...
        
        # Title
        lbl_title = QLabel("📝 Buat Post Baru")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #004d00; margin-bottom: 20px;")
        layout.addWidget(lbl_title)

        # Input Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Masukkan Judul Post (Opsional)")
        self.title_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.title_input)

        # Input Content
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Apa yang ingin kamu bagikan tentang kebunmu?")
        self.content_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px; min-height: 150px;")
        layout.addWidget(self.content_input)

        # Media Status Label
        self.media_status_lbl = QLabel("Tidak ada gambar dipilih.")
        self.media_status_lbl.setStyleSheet("color: #007F00; font-style: italic; margin-top: 5px;")
        
        # --- Tambahkan Tombol Gambar (Sesuai Permintaan) ---
        media_action_layout = QHBoxLayout()
        self.btn_add_media = QPushButton("🖼️ Tambah Gambar")
        self.btn_add_media.setStyleSheet("""
            QPushButton {
                background-color: #E8F5E9; 
                color: #007F00; 
                padding: 5px 10px; 
                border-radius: 5px;
            }
        """)
        self.btn_add_media.clicked.connect(self.select_media_file)

        media_action_layout.addWidget(self.btn_add_media)
        media_action_layout.addWidget(self.media_status_lbl)
        media_action_layout.addStretch(1)
        layout.addLayout(media_action_layout)


        # Action Buttons (Batal/Posting)
        btn_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Batal")
        # ... (Styling Batal) ...
        self.cancel_button.clicked.connect(self.cancel_post) # Ubah connect ke cancel_post
        
        self.submit_button = QPushButton("Posting")
        # ... (Styling Posting) ...
        self.submit_button.clicked.connect(self.submit_post)
        
        btn_layout.addWidget(self.cancel_button)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.submit_button)
        layout.addLayout(btn_layout)

    def select_media_file(self):
        """Membuka dialog untuk memilih file gambar dan menyimpan path."""
        # QFileDialog memerlukan import QFileDialog
        options = QFileDialog.Options()
        # Filter hanya file gambar
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar", "",
                                                   "Gambar Files (*.png *.jpg *.jpeg *.gif);;Semua Files (*)", options=options)
        
        if file_name:
            self.selected_media_path = file_name
            base_name = os.path.basename(file_name)
            self.media_status_lbl.setText(f"Gambar dipilih: {base_name}")
        else:
            self.selected_media_path = ""
            self.media_status_lbl.setText("Tidak ada gambar dipilih.")

    def cancel_post(self):
        """Membersihkan form dan kembali ke feed."""
        self.title_input.clear()
        self.content_input.clear()
        self.selected_media_path = ""
        self.media_status_lbl.setText("Tidak ada gambar dipilih.")
        self.post_manager.switch_to_feed()
        
    def submit_post(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        
        if not content:
            QMessageBox.warning(self, "Peringatan", "Isi post tidak boleh kosong.")
            return

        time_created = QDateTime.currentDateTime().toString(Qt.ISODate)

        # KUNCI: MENGIRIMKAN PATH MEDIA KE ENTITAS POST
        new_post = Post(userID=1, 
                        title=title, 
                        content=content, 
                        media=self.selected_media_path, # <-- Tambahkan path media di sini
                        timeCreated=time_created)
        
        try:
            new_post.createPost(self.post_manager.conn)
            QMessageBox.information(self, "Sukses", "Post berhasil dibuat!")
            self.cancel_post() # Gunakan cancel_post untuk membersihkan form
        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Gagal membuat post: {e}")

# --- PostManager Class (Modifikasi) ---
class PostManager(QWidget):
    def __init__(self, db_path: str = "app.db", parent=None):
        super().__init__(parent)
        
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._setup_db()

        # UI Setup
        self.stackWidget = QStackedWidget()
        
        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # Hapus margin karena akan ditambahkan di DisplayCommunity
        layout.addWidget(self.stackWidget)

        # --- A. FEED LIST PAGE ---
        self.feed_page = QWidget()
        feed_layout = QVBoxLayout(self.feed_page)
        feed_layout.setContentsMargins(0, 0, 0, 0)
        
        # List Widget untuk Post
        # List Widget untuk Post (Ini adalah konten utama)
        self.list_widget = QListWidget()
        # ... (Styling list_widget tetap sama) ...
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        feed_layout.addWidget(self.list_widget)
        
        # Message for no posts
        self.no_post_label = QLabel("Belum ada post di community.\nJadilah yang pertama untuk berbagi!")
        self.no_post_label.setAlignment(Qt.AlignCenter)
        self.no_post_label.setStyleSheet("font-size: 18px; color: #666; padding: 50px;")
        feed_layout.addWidget(self.no_post_label)
        
        self.stackWidget.addWidget(self.feed_page) # Index 0

        # --- B. DETAIL PAGE ---
        self.detail_view = DisplayPost() 
        # ... (Pasang sinyal untuk back, like, reply dari detail view ke PostManager) ...
        self.stackWidget.addWidget(self.detail_view) # Index 1

        # --- C. CREATE POST PAGE ---
        self.create_post_widget = CreatePostWidget(post_manager=self)
        self.stackWidget.addWidget(self.create_post_widget) # Index 2
        
        self.reload_list() # Load post saat inisialisasi
        
    def _setup_db(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            # Mengaktifkan pengembalian baris sebagai dict/nama kolom
            self.conn.row_factory = sqlite3.Row
            Post.create_table(self.conn)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def _setup_tab_button(self, btn: QPushButton, handler):
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #EFEFEF; 
                border: 1px solid #DDD; 
                border-radius: 15px; 
                padding: 5px 15px;
                margin: 5px 5px 15px 0;
            }
            QPushButton:checked {
                background-color: #00A859; 
                color: white; 
                font-weight: bold;
            }
        """)
        btn.clicked.connect(handler)

    def switch_to_create_post(self):
        self.stackWidget.setCurrentWidget(self.create_post_widget)

    def switch_to_feed(self):
        self.stackWidget.setCurrentWidget(self.feed_page)
        self.reload_list() # Kembali dan refresh list

    # ----- UI helpers (Modifikasi reload_list) -----
    def reload_list(self, order_by: str = "timeCreated", limit: Optional[int] = 100):
        if self.conn is None:
            return

        self.list_widget.clear()
        posts = self._load_posts(order_by=order_by, limit=limit)
        
        # Logika menampilkan "Belum ada post"
        if not posts:
            self.no_post_label.show()
            self.list_widget.hide()
        else:
            self.no_post_label.hide()
            self.list_widget.show()
            
            for p in posts:
                # Pastikan hanya menampilkan post utama (repliedPostID IS NULL)
                if p.repliedPostID is not None:
                    continue

                title = p.getTitle() or "(No Title)"
                content_preview = (p.getContent()[:50] + '...') if len(p.getContent()) > 50 else p.getContent()
                
                # Format tampilan di List
                display_text = f"**{title}**\n{content_preview}\n❤️ {p.getLikeCount()} likes"
                
                item = QListWidgetItem(display_text)
                # Simpan postID
                item.setData(Qt.UserRole, p.getPostID())
                self.list_widget.addItem(item)
            
        self.stackWidget.setCurrentIndex(0) # Kembali ke list

    # ... (Sisa metode PostManager tidak berubah) ...
    
    def _on_item_clicked(self, item: QListWidgetItem):
        post_id = item.data(Qt.UserRole)
        self.show_post(post_id)

    def show_post(self, post_id: int):
        # Implementasi seperti yang diberikan
        post = self._get_post(post_id)
        if not post: return
        self._inc_view(post_id)
        post = self._get_post(post_id)
        replies = post.getTotalComments(self.conn) if hasattr(post, "getTotalComments") else 0
        self.detail_view.render_post(post, replies_count=replies)
        self.stackWidget.setCurrentWidget(self.detail_view)

    def _get_post(self, post_id: int) -> Optional[Post]:
        # Implementasi seperti yang diberikan
        get_by_id = getattr(Post, "get_by_id", None) or getattr(Post, "getByID", None)
        if callable(get_by_id):
            return get_by_id(self.conn, post_id)
        cur = self.conn.execute("SELECT * FROM postList WHERE postID = ?", (post_id,))
        row = cur.fetchone()
        return Post.fromRowSQL(row) if row else None

    def _load_posts(self, order_by: str = "timeCreated", limit: Optional[int] = None) -> List[Post]:
        # Modifikasi: Tambahkan filter untuk hanya mengambil post utama (bukan reply)
        mapping = {"timeCreated": "timeCreated", "likes": "likeCount", "views": "viewCount"}
        col = mapping.get(order_by, "timeCreated")
        
        q = f"SELECT * FROM postList WHERE repliedPostID IS NULL ORDER BY {col} DESC"
        params: List[Any] = []
        if limit is not None:
            q += " LIMIT ?"
            params.append(int(limit))
        
        cur = self.conn.execute(q, tuple(params) if params else ())
        rows = cur.fetchall()
        
        return [Post.fromRowSQL(r) for r in rows if Post.fromRowSQL(r) is not None]

    def _inc_view(self, post_id: int):
        post = self._get_post(post_id)
        if post:
            post.incViewCount(self.conn)

    def _inc_like(self, post_id: int):
        post = self._get_post(post_id)
        if post:
            post.incLikeCount(self.conn)