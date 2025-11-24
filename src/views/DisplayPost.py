from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QHBoxLayout, QFrame, QScrollArea, QSpacerItem, QSizePolicy, QStackedWidget, QListWidget, QListWidgetItem)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon
import os
from models.UserModel import DB_FILE_PATH

THIS_FILE = os.path.abspath(__file__)
VIEWS_DIR = os.path.dirname(THIS_FILE)
SRC_DIR = os.path.dirname(VIEWS_DIR)
UPLOAD_DIR = os.path.join(SRC_DIR, "media")

class DisplayPost(QWidget):
    likeRequested = pyqtSignal(int)
    replyRequested = pyqtSignal(int)
    deleteRequested = pyqtSignal(int)
    backRequested = pyqtSignal()

    def __init__(self, db_path: str = DB_FILE_PATH, parent=None):
        super().__init__(parent)
        self.post_id = None
        self.conn = self.parent().conn if self.parent() else None
        self._init_ui() 


    def _init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 20) 

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

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setAlignment(Qt.AlignTop)

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

        # ini buat cek kalau post tersebut adalah hasil sebuah reply post
        self.reply_from_frame = QFrame()
        self.reply_from_frame.setStyleSheet("background-color:#F5F5F5; border-radius:8px; padding:8px;")
        self.reply_from_frame.hide()
        reply_layout = QVBoxLayout(self.reply_from_frame)
        self.reply_from_lbl = QLabel("")
        self.reply_from_lbl.setWordWrap(True)
        reply_layout.addWidget(self.reply_from_lbl)
        card_layout.addWidget(self.reply_from_frame)
        
        author_row = QHBoxLayout()
        
        self.avatar_lbl = QLabel("👤")
        self.avatar_lbl.setFixedSize(45, 45)
        self.avatar_lbl.setAlignment(Qt.AlignCenter)
        self.avatar_lbl.setStyleSheet("background-color: #E8F5E9; border-radius: 22px; font-size: 20px;")
        
        author_text_col = QVBoxLayout()
        author_text_col.setSpacing(2)
        
        name_row = QHBoxLayout()
        self.author_name_lbl = QLabel("John Doe")
        self.author_name_lbl.setStyleSheet("font-weight: bold; font-size: 15px; color: #000; border: none;")
        self.author_handle_lbl = QLabel("@johndoe")
        self.author_handle_lbl.setStyleSheet("color: gray; font-size: 13px; border: none;")
        
        name_row.addWidget(self.author_name_lbl)
        name_row.addWidget(self.author_handle_lbl)
        name_row.addStretch()
        
        self.time_lbl = QLabel("2 hours ago")
        self.time_lbl.setStyleSheet("color: gray; font-size: 12px; border: none;")
        
        author_text_col.addLayout(name_row)
        author_text_col.addWidget(self.time_lbl)
        
        author_row.addWidget(self.avatar_lbl)
        author_row.addLayout(author_text_col)
        author_row.addStretch()
        
        card_layout.addLayout(author_row)

        self.title_lbl = QLabel()
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #000; border: none; margin-top: 5px;")
        self.title_lbl.hide() 
        card_layout.addWidget(self.title_lbl)
        
        self.content_lbl = QLabel("Content goes here...")
        self.content_lbl.setWordWrap(True)
        self.content_lbl.setStyleSheet("font-size: 16px; color: #333; line-height: 1.4; border: none; margin-top: 10px;")
        card_layout.addWidget(self.content_lbl)

        self.media_container = QLabel()
        self.media_container.setScaledContents(False)
        self.media_container.setAlignment(Qt.AlignCenter)
        self.media_container.setStyleSheet("background-color: #F5F5F5; border-radius: 12px;")
        self.media_container.setMaximumHeight(400)
        self.media_container.hide() 
        card_layout.addWidget(self.media_container)

        self.stats_lbl = QLabel("")
        self.stats_lbl.setStyleSheet("color: gray; font-size: 13px; margin-top: 10px; border: none;")
        card_layout.addWidget(self.stats_lbl)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #EEEEEE; border: none; max-height: 1px;")
        card_layout.addWidget(line)

        actions_row = QHBoxLayout()
        actions_row.setSpacing(30)

        def create_action_btn(icon, text):
            btn = QPushButton(f"{icon} {text}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { background: transparent; border: none; font-size: 16px; color: #666; padding: 8px 16px; }
                QPushButton:hover { color: #007F00; background-color: #E8F5E9; border-radius: 20px; }
            """)
            btn.setMinimumWidth(110)
            btn.setMinimumHeight(44)
            return btn

        self.btn_reply = create_action_btn("💬", "Reply")
        self.btn_like = create_action_btn("❤️","Like")
        self.views_lbl = QLabel("0 Views")
        self.views_lbl.setStyleSheet("color: #666; font-size: 15px; padding: 8px;")
        self.views_lbl.setAlignment(Qt.AlignCenter)
        self.views_lbl.setMinimumHeight(44)
        self.views_lbl.setMinimumWidth(100)

        actions_row.addWidget(self.btn_reply)
        actions_row.addWidget(self.btn_like)
        actions_row.addStretch()
        actions_row.addWidget(self.views_lbl)

        card_layout.addLayout(actions_row)

        content_layout.addWidget(self.card)
        content_layout.addStretch()
        
        scroll.setWidget(content_container)
        self.main_layout.addWidget(scroll)

        self.back_btn.clicked.connect(lambda: self.backRequested.emit())
        self.btn_like.clicked.connect(lambda: self._emit_if_set(self.likeRequested))
        self.btn_reply.clicked.connect(lambda: self._emit_if_set(self.replyRequested))

    def _emit_if_set(self, sig):
        if self.post_id is not None:
            sig.emit(self.post_id)

    def clear(self):
        self.post_id = None
        self.author_name_lbl.setText("")
        self.author_handle_lbl.setText("")
        self.title_lbl.setText("")
        self.title_lbl.hide()
        self.content_lbl.setText("")
        self.stats_lbl.setText("")
        self.media_container.clear()
        self.media_container.hide()
        self.reply_from_frame.hide()
        # reset like button style
        self.btn_like.setStyleSheet("""
            QPushButton { background: transparent; border: none; font-size: 16px; color: #666; padding: 8px 16px; }
            QPushButton:hover { color: #007F00; background-color: #E8F5E9; border-radius: 20px; }
        """)
    
    def render_post(self, post, replies_count: int = 0):
        if post is None:
            self.clear()
            return

        self.post_id = post.getPostID()
        
        from models.Post import Post as PostModel
        
        # show if this post is a reply from another post
        if post.repliedPostID:
            parent = PostModel.get_by_id(self.conn, post.repliedPostID)
            if parent:
                author = PostModel.getUsernameByID(self.conn, parent.getAuthor())
                title = parent.getTitle() or "(no title)"
                self.reply_from_lbl.setText(f"Reply from post \"{title}\" by {author}")
                self.reply_from_frame.show()
            else:
                self.reply_from_frame.hide()
        else:
            self.reply_from_frame.hide()

        author_name = None
        if hasattr(self.parent(), 'user_model') and self.parent().user_model.userID == post.getAuthor():
            author_name = self.parent().user_model.username
        elif self.conn:
            author_name = PostModel.getUsernameByID(self.conn, post.getAuthor())

        if not author_name:
            author_name = f"User {post.getAuthor()}"
            
        handle = f"@{author_name.lower().replace(' ', '')}"
        
        self.author_name_lbl.setText(author_name)
        self.author_handle_lbl.setText(handle)
        
        if post.getTitle():
            self.title_lbl.setText(post.getTitle())
            self.title_lbl.show()
        else :
            self.title_lbl.hide()
        
        self.content_lbl.setText(post.getContent())
        
        self.stats_lbl.setText(f"{replies_count} Replies • {post.getLikeCount()} Likes")
        self.views_lbl.setText(f"{post.getViewCount()} Views")

        # ini buat nunjukin kalau post udah di like atau belum
        liked = False
        if self.conn and hasattr(self.parent(), 'user_model'):
            try:
                liked = PostModel.has_user_liked(self.conn, post.getPostID(), self.parent().user_model.userID)
            except Exception:
                liked = False

        if liked:
            self.btn_like.setStyleSheet("""
                QPushButton { background: transparent; border: none; font-size: 16px; color: #E91E63; padding: 8px 16px; }
                QPushButton:hover { color: #E91E63; background-color: #FDEBF0; border-radius: 20px; }
            """)
        else:
            # default
            self.btn_like.setStyleSheet("""
                QPushButton { background: transparent; border: none; font-size: 16px; color: #666; padding: 8px 16px; }
                QPushButton:hover { color: #007F00; background-color: #E8F5E9; border-radius: 20px; }
            """)

        media_value = post.media or ""
        media_path = ""
        if media_value:
            if os.path.isabs(media_value):
                media_path = media_value
            else:
                media_path = os.path.join(UPLOAD_DIR, media_value)

        if media_path and os.path.isfile(media_path):
            pix = QPixmap(media_path)
            if not pix.isNull():
                scaled_pix = pix.scaled(800, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.media_container.setPixmap(scaled_pix)
                self.media_container.setFixedHeight(scaled_pix.height())
                self.media_container.show()
            else:
                self.media_container.hide()
        else:
            self.media_container.hide()
            