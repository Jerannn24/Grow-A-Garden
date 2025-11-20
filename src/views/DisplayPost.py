from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QHBoxLayout, QFrame, QScrollArea, QSpacerItem, QSizePolicy, QStackedWidget, QListWidget, QlistWidgetItem)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon
import os
from models.UserModel import DB_FILE_PATH

class DisplayPost(QWidget):
    # Signals
    likeRequested = pyqtSignal(int)
    replyRequested = pyqtSignal(int)
    deleteRequested = pyqtSignal(int)
    backRequested = pyqtSignal()

    def __init__(self, db_path: str = DB_FILE_PATH, parent=None):
        super().__init__(parent)
        # ... (koneksi DB sama seperti sebelumnya) ...

        # UI Setup
        self.stackWidget = QStackedWidget()
        
        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 0) # Memberi margin agar tidak mepet sidebar
        layout.addWidget(self.stackWidget)

        # --- A. FEED LIST PAGE ---
        self.feed_page = QWidget()
        feed_layout = QVBoxLayout(self.feed_page)
        feed_layout.setContentsMargins(0,0,0,0)
        
        # Title Feed
        lbl = QLabel("Community Feed")
        lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #004d00; margin-bottom: 10px;")
        feed_layout.addWidget(lbl)
        
        self.list_widget = QListWidget()
        # Styling List agar tidak terlihat seperti aplikasi tahun 90an
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 10px;
                border: 1px solid #ddd;
                color: #333;
            }
            QListWidget::item:hover {
                background-color: #f9f9f9;
                border-color: #007F00;
            }
            QListWidget::item:selected {
                background-color: #E8F5E9;
                color: #000;
                border: 1px solid #007F00;
            }
        """)
        feed_layout.addWidget(self.list_widget)
        
        self.stackWidget.addWidget(self.feed_page) # Index 0

        # --- B. DETAIL PAGE ---
        self.detail_view = DisplayPost() # Ini akan menggunakan Class baru di atas
        self.stackWidget.addWidget(self.detail_view) # Index 1

        # ... (Koneksi sinyal sama seperti sebelumnya) ...

    def _init_ui(self):
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- 1. Header (Back Button & Title) ---
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 20) # Margin bottom

        self.back_btn = QPushButton("←")
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton { border: none; font-size: 24px; color: #007F00; font-weight: bold; }
            QPushButton:hover { color: #005500; }
        """)
        
        header_title = QLabel("Post")
        header_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        header_layout.addWidget(self.back_btn)
        header_layout.addSpacing(10)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        self.main_layout.addWidget(header_frame)

        # --- 2. Scroll Area (Agar konten panjang bisa discroll) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setAlignment(Qt.AlignTop)

        # --- 3. POST CARD (Kotak Putih) ---
        self.card = QFrame()
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #E0E0E0;
            }
        """)
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        # A. Author Info (Avatar, Name, Handle, Time)
        author_row = QHBoxLayout()
        
        # Avatar (Lingkaran dummy)
        self.avatar_lbl = QLabel("👤")
        self.avatar_lbl.setFixedSize(45, 45)
        self.avatar_lbl.setAlignment(Qt.AlignCenter)
        self.avatar_lbl.setStyleSheet("background-color: #E8F5E9; border-radius: 22px; font-size: 20px;")
        
        author_text_col = QVBoxLayout()
        author_text_col.setSpacing(2)
        
        # Name & Handle container
        name_row = QHBoxLayout()
        self.author_name_lbl = QLabel("John Doe")
        self.author_name_lbl.setStyleSheet("font-weight: bold; font-size: 15px; color: #000; border: none;")
        self.author_handle_lbl = QLabel("@johndoe")
        self.author_handle_lbl.setStyleSheet("color: gray; font-size: 13px; border: none;")
        
        name_row.addWidget(self.author_name_lbl)
        name_row.addWidget(self.author_handle_lbl)
        name_row.addStretch()
        
        # Time
        self.time_lbl = QLabel("2 hours ago")
        self.time_lbl.setStyleSheet("color: gray; font-size: 12px; border: none;")
        
        author_text_col.addLayout(name_row)
        author_text_col.addWidget(self.time_lbl)
        
        author_row.addWidget(self.avatar_lbl)
        author_row.addLayout(author_text_col)
        author_row.addStretch()
        
        card_layout.addLayout(author_row)

        # B. Post Content (Text)
        self.content_lbl = QLabel("Content goes here...")
        self.content_lbl.setWordWrap(True)
        self.content_lbl.setStyleSheet("font-size: 16px; color: #333; line-height: 1.4; border: none; margin-top: 10px;")
        card_layout.addWidget(self.content_lbl)

        # C. Media (Image)
        self.media_container = QLabel()
        self.media_container.setScaledContents(True)
        self.media_container.setAlignment(Qt.AlignCenter)
        self.media_container.setStyleSheet("background-color: #F5F5F5; border-radius: 12px;")
        self.media_container.setFixedHeight(250) # Default height, bisa dihide
        self.media_container.hide() # Hide by default
        card_layout.addWidget(self.media_container)

        # D. Stats (Replies, Retweets, Likes)
        stats_row = QHBoxLayout()
        self.stats_lbl = QLabel("0 Replies   0 Retweets   0 Likes")
        self.stats_lbl.setStyleSheet("color: gray; font-size: 13px; margin-top: 10px; border: none;")
        stats_row.addWidget(self.stats_lbl)
        stats_row.addStretch()
        card_layout.addLayout(stats_row)
        
        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #EEEEEE; border: none; max-height: 1px;")
        card_layout.addWidget(line)

        # E. Action Buttons (Reply, Retweet, Like, Share)
        actions_row = QHBoxLayout()
        actions_row.setSpacing(30)
        
        # Helper to create icon buttons
        def create_action_btn(icon_text):
            btn = QPushButton(icon_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { background: transparent; border: none; font-size: 18px; color: #666; }
                QPushButton:hover { color: #007F00; background-color: #E8F5E9; border-radius: 15px; }
            """)
            btn.setFixedSize(40, 40)
            return btn

        self.btn_reply = create_action_btn("💬") # Chat bubble
        self.btn_retweet = create_action_btn("🔁") # Loop
        self.btn_like = create_action_btn("❤️") # Heart
        self.btn_share = create_action_btn("📤") # Upload
        
        # Delete button (special case)
        self.btn_delete = create_action_btn("🗑️")

        actions_row.addWidget(self.btn_reply)
        actions_row.addWidget(self.btn_retweet)
        actions_row.addWidget(self.btn_like)
        actions_row.addWidget(self.btn_share)
        actions_row.addStretch()
        actions_row.addWidget(self.btn_delete) # Layout delete di kanan

        card_layout.addLayout(actions_row)

        # Add Card to Content Layout
        content_layout.addWidget(self.card)
        content_layout.addStretch() # Push card to top
        
        scroll.setWidget(content_container)
        self.main_layout.addWidget(scroll)

        # Connections
        self.back_btn.clicked.connect(lambda: self.backRequested.emit())
        self.btn_like.clicked.connect(lambda: self._emit_if_set(self.likeRequested))
        self.btn_reply.clicked.connect(lambda: self._emit_if_set(self.replyRequested))
        self.btn_delete.clicked.connect(lambda: self._emit_if_set(self.deleteRequested))

    def _emit_if_set(self, sig):
        if self.post_id is not None:
            sig.emit(self.post_id)

    def render_post(self, post, replies_count: int = 0):
        if post is None:
            self.clear()
            return

        self.post_id = post.getPostID()
        
        # 1. Set Text Data
        # Author: Karena di DB hanya ada UserID (int), kita mock dulu atau perlu query User
        # Disini saya pakai placeholder logika
        author_name = f"User {post.getAuthor()}" 
        handle = f"@{getattr(post, 'handle', 'emmaplants')}" # Gunakan placeholder handle jika tidak ada
        
        self.author_name_lbl.setText(author_name)
        self.author_handle_lbl.setText(handle)
        
        # Pastikan Title dan Content muncul
        full_content = ""
        if post.getTitle():
            full_content += f"**{post.getTitle()}**\n\n"
        full_content += post.getContent()
        
        self.content_lbl.setText(full_content) # Menggunakan full_content yang menyertakan title
        
        # 2. Set Stats
        self.stats_lbl.setText(f"{replies_count} Replies   {post.getViewCount()} Views   {post.getLikeCount()} Likes")
        
        # 3. Set Media (Image)
        media_path = post.media # Mengambil langsung dari field media
        if media_path and os.path.isfile(media_path):
            pix = QPixmap(media_path)
            self.media_container.setPixmap(pix.scaled(self.media_container.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.media_container.show()
        else:
            # Jika tidak ada gambar, tampilkan placeholder/sembunyikan container
            self.media_container.setText("🍅") # Placeholder seperti gambar kedua
            self.media_container.setFixedHeight(250)
            self.media_container.show() # Tampilkan placeholder jika Anda menginginkan visual seperti gambar kedua
            