import sqlite3
import sys
import os
from typing import Optional, List, Any
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, QListWidget, 
                             QListWidgetItem, QApplication, QLabel, QPushButton, 
                             QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QDateTime
from models.UserModel import DB_FILE_PATH
# ============================================
# PATH CONFIGURATION
# ============================================
THIS_FILE = os.path.abspath(__file__)
CONTROLLERS_DIR = os.path.dirname(THIS_FILE)
SRC_DIR = os.path.dirname(CONTROLLERS_DIR)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# ============================================
# IMPORTS
# ============================================
try:
    from views.DisplayPost import DisplayPost
except ImportError:
    class DisplayPost(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setLayout(QVBoxLayout())
            self.layout().addWidget(QLabel("DisplayPost tidak ditemukan"))
        
        def render_post(self, post, replies_count=0):
            pass

try:
    from models.Post import Post
except ImportError:
    print("ERROR: models.Post tidak dapat diimport")
    sys.exit(1)

# --- CREATE POST WIDGET ---
class CreatePostWidget(QWidget):
    def __init__(self, post_manager, parent=None):
        super().__init__(parent)
        self.post_manager = post_manager
        self.selected_media_path: str = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
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
        
        # Media Button
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

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Batal")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #666;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        self.cancel_button.clicked.connect(self.cancel_post)
        
        self.submit_button = QPushButton("Posting")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #007F00;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #006600;
            }
        """)
        self.submit_button.clicked.connect(self.submit_post)
        
        btn_layout.addWidget(self.cancel_button)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.submit_button)
        layout.addLayout(btn_layout)

    def select_media_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Pilih Gambar", "",
            "Gambar Files (*.png *.jpg *.jpeg *.gif);;Semua Files (*)", 
            options=options
        )
        
        if file_name:
            self.selected_media_path = file_name
            base_name = os.path.basename(file_name)
            self.media_status_lbl.setText(f"Gambar dipilih: {base_name}")
        else:
            self.selected_media_path = ""
            self.media_status_lbl.setText("Tidak ada gambar dipilih.")

    def cancel_post(self):
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

        new_post = Post(
            userID=1, 
            title=title, 
            content=content, 
            media=self.selected_media_path,
            timeCreated=time_created
        )
        
        try:
            new_post.createPost(self.post_manager.conn)
            QMessageBox.information(self, "Sukses", "Post berhasil dibuat!")
            self.cancel_post()
        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Gagal membuat post: {e}")

# --- POST MANAGER ---
class PostManager(QWidget):
    def __init__(self, db_path: str = DB_FILE_PATH, parent=None):
        super().__init__(parent)
        
        # Pastikan db_path adalah absolute path
        if not os.path.isabs(db_path):
            db_path = os.path.join(SRC_DIR, db_path)
        
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._setup_db()

        # UI Setup
        self.stackWidget = QStackedWidget()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stackWidget)

        # --- FEED PAGE ---
        self.feed_page = QWidget()
        feed_layout = QVBoxLayout(self.feed_page)
        feed_layout.setContentsMargins(0, 0, 0, 0)
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 5px 0;
                border: 1px solid #E0E0E0;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        feed_layout.addWidget(self.list_widget)
        
        self.no_post_label = QLabel("Belum ada post di community.\nJadilah yang pertama untuk berbagi!")
        self.no_post_label.setAlignment(Qt.AlignCenter)
        self.no_post_label.setStyleSheet("font-size: 18px; color: #666; padding: 50px;")
        feed_layout.addWidget(self.no_post_label)
        
        self.stackWidget.addWidget(self.feed_page)

        # --- DETAIL PAGE ---
        self.detail_view = DisplayPost()
        self.stackWidget.addWidget(self.detail_view)

        # --- CREATE POST PAGE ---
        self.create_post_widget = CreatePostWidget(post_manager=self)
        self.stackWidget.addWidget(self.create_post_widget)
        
        self.reload_list()
        
    def _setup_db(self):
        try:
            print(f"📊 Connecting to database: {self.db_path}")
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            Post.create_table(self.conn)
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            self.conn = None

    def switch_to_create_post(self):
        self.stackWidget.setCurrentWidget(self.create_post_widget)

    def switch_to_feed(self):
        self.stackWidget.setCurrentWidget(self.feed_page)
        self.reload_list()

    def reload_list(self, order_by: str = "timeCreated", limit: Optional[int] = 100):
        if self.conn is None:
            print("⚠️  Koneksi database tidak tersedia")
            return

        self.list_widget.clear()
        posts = self._load_posts(order_by=order_by, limit=limit)
        
        if not posts:
            self.no_post_label.show()
            self.list_widget.hide()
        else:
            self.no_post_label.hide()
            self.list_widget.show()
            
            for p in posts:
                if p.repliedPostID is not None:
                    continue

                title = p.getTitle() or "(No Title)"
                content_preview = (p.getContent()[:50] + '...') if len(p.getContent()) > 50 else p.getContent()
                
                display_text = f"**{title}**\n{content_preview}\n❤️ {p.getLikeCount()} likes | 👁️ {p.getViewCount()} views"
                
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, p.getPostID())
                self.list_widget.addItem(item)
            
        self.stackWidget.setCurrentIndex(0)
    
    def _on_item_clicked(self, item: QListWidgetItem):
        post_id = item.data(Qt.UserRole)
        self.show_post(post_id)

    def show_post(self, post_id: int):
        post = self._get_post(post_id)
        if not post:
            return
        self._inc_view(post_id)
        post = self._get_post(post_id)
        replies = post.getTotalComments(self.conn) if hasattr(post, "getTotalComments") else 0
        self.detail_view.render_post(post, replies_count=replies)
        self.stackWidget.setCurrentWidget(self.detail_view)

    def _get_post(self, post_id: int) -> Optional[Post]:
        if self.conn is None:
            return None
        get_by_id = getattr(Post, "get_by_id", None) or getattr(Post, "getByID", None)
        if callable(get_by_id):
            return get_by_id(self.conn, post_id)
        cur = self.conn.execute("SELECT * FROM postList WHERE postID = ?", (post_id,))
        row = cur.fetchone()
        return Post.fromRowSQL(row) if row else None

    def _load_posts(self, order_by: str = "timeCreated", limit: Optional[int] = None) -> List[Post]:
        if self.conn is None:
            return []
        
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