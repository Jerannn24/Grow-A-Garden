import sqlite3
import sys
import os
from typing import Optional, List, Any
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, QListWidget, 
                             QListWidgetItem, QApplication, QLabel, QPushButton, 
                             QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon

# path
THIS_FILE = os.path.abspath(__file__)
CONTROLLERS_DIR = os.path.dirname(THIS_FILE)
SRC_DIR = os.path.dirname(CONTROLLERS_DIR)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

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
    from models.UserModel import UserModel
except ImportError:
    print("ERROR: models.Post atau model.UserModel tidak dapat diimport")
    sys.exit(1)

class CreatePostWidget(QWidget):
    def __init__(self, post_manager, parent=None):
        super().__init__(parent)
        self.post_manager = post_manager
        self.selected_media_path: str = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        lbl_title = QLabel("📝 Buat Post Baru")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #004d00; margin-bottom: 20px;")
        layout.addWidget(lbl_title)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Masukkan Judul Post (Opsional)")
        self.title_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.title_input)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Apa yang ingin kamu bagikan tentang kebunmu?")
        self.content_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px; min-height: 150px;")
        layout.addWidget(self.content_input)

        self.media_status_lbl = QLabel("Tidak ada gambar dipilih.")
        self.media_status_lbl.setStyleSheet("color: #007F00; font-style: italic; margin-top: 5px;")
        
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
        
        currentUser = self.post_manager.user_model.getCurrentUser()
        user_id = currentUser.get("userID") if currentUser else None
        
        time_created = QDateTime.currentDateTime().toString(Qt.ISODate)

        new_post = Post(
            userID=user_id, 
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

class PostManager(QWidget):
    def __init__(self, db_path: str = "app.db", parent=None):
        super().__init__(parent)
        
        if not os.path.isabs(db_path):
            db_path = os.path.join(SRC_DIR, db_path)
        
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.user_model = UserModel()
        self._setup_db()

        self.stackWidget = QStackedWidget()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stackWidget)

        # Halaman feed
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
                padding: 0px;
                margin: 10px 0;
                border: 1px solid #E0E0E0;
                min-height: 140px;
            }
            QListWidget::item:hover {
                background-color: #F9F9F9;
                border-color: #007F00;
                cursor: pointer;
            }
            QListWidget::item:selected {
                background-color: #E8F5E9;
                border-color: #007F00;
            }
        """)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        feed_layout.addWidget(self.list_widget)
        
        self.no_post_label = QLabel("Belum ada post di community.\nJadilah yang pertama untuk berbagi!")
        self.no_post_label.setAlignment(Qt.AlignCenter)
        self.no_post_label.setStyleSheet("font-size: 18px; color: #666; padding: 50px;")
        feed_layout.addWidget(self.no_post_label)
        
        self.stackWidget.addWidget(self.feed_page)

        self.detail_view = DisplayPost()
        self.stackWidget.addWidget(self.detail_view)

        # create post
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
        posts = Post.get_all_posts(self.conn, order_by=order_by, limit=limit)
        
        posts = [p for p in posts if p.repliedPostID is None]
        
        if not posts:
            self.no_post_label.show()
            self.list_widget.hide()
        else:
            self.no_post_label.hide()
            self.list_widget.show()
            
            for p in posts:
                username = Post.getUsernameByID(self.conn, p.getAuthor())
                title = p.getTitle() or ""
                content = p.getContent() or ""
            
                content_preview = (content[:100] + '...') if len(content) > 100 else content
                
                if title:
                    display_text = f"""
                    <div style='padding: 5px;'>
                        <p style='font-size: 14px; color: #666; margin: 0 0 10px 0;'>
                            <span style='color: #007F00; font-weight: bold;'>👤 {username}</span>
                        </p>
                        <p style='font-size: 18px; font-weight: bold; color: #1a1a1a; margin: 0 0 12px 0;'>
                            {title}
                        </p>
                        <p style='font-size: 15px; color: #333; margin: 0 0 15px 0; line-height: 1.5;'>
                            {content_preview}
                        </p>
                        <p style='font-size: 13px; color: #888; margin: 0;'>
                            <span style='color: #E91E63;'>❤️ {p.getLikeCount()}</span>  •  
                            <span style='color: #2196F3;'>👁️ {p.getViewCount()}</span>
                        </p>
                    </div>
                    """
                else:
                    display_text = f"""
                    <div style='padding: 5px;'>
                        <p style='font-size: 14px; color: #666; margin: 0 0 10px 0;'>
                            <span style='color: #007F00; font-weight: bold;'>👤 {username}</span>
                        </p>
                        <p style='font-size: 15px; color: #333; margin: 0 0 15px 0; line-height: 1.5;'>
                            {content_preview}
                        </p>
                        <p style='font-size: 13px; color: #888; margin: 0;'>
                            <span style='color: #E91E63;'>❤️ {p.getLikeCount()}</span>  •  
                            <span style='color: #2196F3;'>👁️ {p.getViewCount()}</span>
                        </p>
                    </div>
                    """
                
                item = QListWidgetItem()
                item.setData(Qt.UserRole, p.getPostID())
                
                widget = QWidget()
                widget_layout = QVBoxLayout(widget)
                widget_layout.setContentsMargins(15, 15, 15, 15)
                widget_layout.setSpacing(0)
                
                label = QLabel(display_text)
                label.setWordWrap(True)
                label.setTextFormat(Qt.RichText)
                widget_layout.addWidget(label)
            
                item.setSizeHint(widget.sizeHint())
                
                self.list_widget.addItem(item)
                self.list_widget.setItemWidget(item, widget)
            
        self.stackWidget.setCurrentIndex(0)

    
    def _on_item_clicked(self, item: QListWidgetItem):
        post_id = item.data(Qt.UserRole)
        self.show_post(post_id)

    def show_post(self, post_id: int):
        post = Post.get_by_id(self.conn, post_id)
        if not post:
            return
        
        post.incViewCount(self.conn)
        post = Post.get_by_id(self.conn, post_id) 
        replies = post.getTotalComments(self.conn) 
        
        self.detail_view.render_post(post, replies_count=replies)
        self.stackWidget.setCurrentWidget(self.detail_view)