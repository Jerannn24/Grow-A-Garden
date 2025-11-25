from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QHBoxLayout, QFrame, QScrollArea, QSpacerItem, QSizePolicy, QStackedWidget, QListWidget, QListWidgetItem, QDialog)
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QIcon
import os
from typing import List, TYPE_CHECKING, Any 
from models.UserModel import DB_FILE_PATH

THIS_FILE = os.path.abspath(__file__)
VIEWS_DIR = os.path.dirname(THIS_FILE)
SRC_DIR = os.path.dirname(VIEWS_DIR)
UPLOAD_DIR = os.path.join(SRC_DIR, "media")
PUBLIC_DIR = os.path.join(SRC_DIR, "public")

ICON_RED_HEART = os.path.join(PUBLIC_DIR, "heart_red.png")
ICON_GREY_HEART = os.path.join(PUBLIC_DIR, "heart_grey.jpg")

if TYPE_CHECKING:
    from models.Post import Post as PostModel
else:
    from models.Post import Post as PostModel

try:
    from views.ReportForm import ReportForm
    from models.Report import Report
except ImportError:
    ReportForm = None
    Report = None


class DisplayPost(QWidget):
    likeRequested = pyqtSignal(int)
    replyRequested = pyqtSignal(int)
    deleteRequested = pyqtSignal(int)
    backRequested = pyqtSignal()
    showReplyDetailRequested = pyqtSignal(int)

    def __init__(self, db_path: str = DB_FILE_PATH, parent=None):
        super().__init__(parent)
        self.post_id = None
        self.post_manager = None
        current = parent
        while current:
            if hasattr(current, 'user_model') and hasattr(current, 'conn'):
                self.post_manager = current
                break
            current = current.parent() if hasattr(current, 'parent') else None
        
        if self.post_manager and hasattr(self.post_manager, 'conn'):
            self.conn = self.post_manager.conn
        else:
            self.conn = None
        self.icon_red = QIcon(ICON_RED_HEART)
        self.icon_grey = QIcon(ICON_GREY_HEART)
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

        # Report button (kanan atas)
        self.report_btn = QPushButton("⚠️ Laporkan")
        self.report_btn.setCursor(Qt.PointingHandCursor)
        self.report_btn.setToolTip("Laporkan Post")
        self.report_btn.setStyleSheet("""
            QPushButton { 
                border: 1px solid #FF6B6B;
                font-size: 12px; 
                color: #FF6B6B; 
                background-color: white;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover { 
                background-color: #FFF5F5;
                color: #FF4444;
                border-color: #FF4444;
            }
        """)
        self.report_btn.clicked.connect(self._open_report_form)
        self.report_btn.hide() 
        
        header_layout.addWidget(self.back_btn)
        header_layout.addSpacing(10)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.report_btn)
        
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
        self.btn_like = QPushButton("Like")
        self.btn_like.setCursor(Qt.PointingHandCursor)
        self.btn_like.setStyleSheet("""
            QPushButton { 
                background: transparent; border: none; font-size: 16px; color: #666; 
                padding: 8px 16px; 
                text-align: left;
            }
            QPushButton:hover { background-color: #E8F5E9; border-radius: 20px; }
        """)
        self.btn_like.setMinimumWidth(110)
        self.btn_like.setMinimumHeight(44)
        iconSize = 24
        self.btn_like.setIconSize(QSize(iconSize,iconSize))
        
        self.btn_like.setIcon(self.icon_grey)
        
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

        self.reply_section = QFrame()
        self.reply_section.setStyleSheet("background-color: transparent;")
        self.reply_layout = QVBoxLayout(self.reply_section)
        self.reply_layout.setContentsMargins(25, 20, 25, 0)
        self.reply_layout.setSpacing(10)
        
        self.replies_header_lbl = QLabel("Replies (0)")
        self.replies_header_lbl.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 5px; color: #333;")
        self.reply_layout.addWidget(self.replies_header_lbl)
        
        self.replies_list_widget = QListWidget()
        self.replies_list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
            }
            QListWidget::item {
                border-bottom: 1px solid #E0E0E0;
                padding: 10px 0;
            }
            QListWidget::item:hover {
                background-color: #F8F8F8;
            }
        """)
        self.replies_list_widget.setMinimumHeight(50)
        self.replies_list_widget.setMaximumHeight(600)
        self.replies_list_widget.setFrameShape(QFrame.NoFrame)
        self.replies_list_widget.itemClicked.connect(self._on_reply_item_clicked) 
        self.reply_layout.addWidget(self.replies_list_widget)

        content_layout.addWidget(self.reply_section)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_container)
        self.main_layout.addWidget(scroll)

        self.back_btn.clicked.connect(lambda: self.backRequested.emit())
        self.btn_like.clicked.connect(lambda: self._emit_if_set(self.likeRequested))
        self.btn_reply.clicked.connect(lambda: self._emit_if_set(self.replyRequested))

    def _emit_if_set(self, sig):
        if self.post_id is not None:
            sig.emit(self.post_id)

    def _on_reply_item_clicked(self, item: QListWidgetItem):
        post_id = item.data(Qt.UserRole)
        if post_id is not None:
            self.showReplyDetailRequested.emit(post_id)
    
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
        self.replies_list_widget.clear()
        self.replies_header_lbl.setText("Replies (0)")
        self.btn_like.setIcon(self.icon_grey)
        self.btn_like.setStyleSheet("""
            QPushButton { 
                background: transparent; border: none; font-size: 16px; color: #666; padding: 8px 16px; 
                text-align: left;
            }
            QPushButton:hover { color: #007F00; background-color: #E8F5E9; border-radius: 20px; }
        """)
        self.report_btn.hide()
        
    def _render_replies(self, replies: List[PostModel]):
        self.replies_list_widget.clear()
        self.replies_header_lbl.setText(f"Replies ({len(replies)})")

        for reply in replies:
            author_name = PostModel.getUsernameByID(self.conn, reply.getAuthor())
            content = reply.getContent() or ""
            content_preview = (content[:150] + '...') if len(content) > 150 else content
            
            item = QListWidgetItem()
            item.setData(Qt.UserRole, reply.getPostID())
            
            widget = QWidget()
            widget.setCursor(Qt.PointingHandCursor)
            
            reply_html = f"""
            <div style="padding: 10px 0; ">
                <span style='color: #007F00; font-weight: bold; font-size: 15px;'>👤 {author_name}</span>
                <span style='color: gray; font-size: 12px;'> &bull; {reply.timeCreated}</span>
                <div style='font-size: 14px; color: #333; margin-top: 5px; line-height: 1.4;'>{content_preview}</div>
                <div style='font-size: 12px; color: #999; margin-top: 5px;'>💬 {reply.getTotalComments(self.conn)} | ❤️ {reply.getLikeCount()}</div> 
            </div>
            """
            
            label = QLabel(reply_html)
            label.setWordWrap(True)
            label.setTextFormat(Qt.RichText)
            label.setAttribute(Qt.WA_TransparentForMouseEvents)
            
            widget_layout = QVBoxLayout(widget)
            widget_layout.setContentsMargins(0, 0, 0, 0)
            widget_layout.addWidget(label)
            
            label.adjustSize()
            item.setSizeHint(QSize(self.replies_list_widget.sizeHint().width(), label.sizeHint().height() + 10))
            
            self.replies_list_widget.addItem(item)
            self.replies_list_widget.setItemWidget(item, widget)
            
    def render_post(self, post, replies_count: int = 0):
        if post is None:
            self.clear()
            return

        self.post_id = post.getPostID()
        
        if post.repliedPostID:
            parent = PostModel.get_by_id(self.conn, post.repliedPostID)
            if parent:
                author = PostModel.getUsernameByID(self.conn, parent.getAuthor())

                if getattr(parent, 'isAvailable', 1) == 0:
                    title = "Unavailable"
                else:
                    title = parent.getTitle() or "(No Title)"
                self.reply_from_lbl.setText(f"Reply from post \"{title}\" by {author}")
                self.reply_from_frame.show()
            else:
                self.reply_from_frame.hide()
        else:
            self.reply_from_frame.hide()

        author_name = None
        if self.post_manager and hasattr(self.post_manager, 'user_model') and self.post_manager.user_model and self.post_manager.user_model.userID == post.getAuthor():
            author_name = self.post_manager.user_model.username
        elif self.conn:
            author_name = PostModel.getUsernameByID(self.conn, post.getAuthor())

        if not author_name:
            author_name = f"User {post.getAuthor()}"
            
        handle = f"@{author_name.lower().replace(' ', '')}"
        
        self.author_name_lbl.setText(author_name)
        self.author_handle_lbl.setText(handle)
        
        user_model = None
        if self.post_manager and hasattr(self.post_manager, 'user_model'):
            user_model = self.post_manager.user_model
        
        show_report_btn = False
        if user_model and hasattr(user_model, 'userID'):
            try:
                user_id = user_model.userID
                post_author_id = post.getAuthor()
                
                if user_id is not None and post_author_id is not None and user_id != post_author_id:
                    show_report_btn = True
            except Exception as e:
                print(f"⚠️ Error checking report button visibility: {e}")
        
        self.report_btn.setVisible(show_report_btn)
        
        if post.getTitle():
            self.title_lbl.setText(post.getTitle())
            self.title_lbl.show()
        else :
            self.title_lbl.hide()
        
        self.content_lbl.setText(post.getContent())
        
        all_replies = post.getAllComments(self.conn)
        self.stats_lbl.setText(f"{len(all_replies)} Replies • {post.getLikeCount()} Likes")
        self._render_replies(all_replies) 
        
        self.views_lbl.setText(f"{post.getViewCount()} Views")

        # ini buat nunjukin kalau post udah di like atau belum
        liked = False
        if self.conn and self.post_manager and hasattr(self.post_manager, 'user_model') and self.post_manager.user_model:
            try:
                liked = PostModel.has_user_liked(self.conn, post.getPostID(), self.post_manager.user_model.userID)
            except Exception:
                liked = False

        if liked:
            self.btn_like.setIcon(self.icon_red)
            self.btn_like.setStyleSheet("""
                QPushButton { 
                    background: transparent; border: none; font-size: 16px; color: #666; padding: 8px 16px; 
                    text-align: left;
                }
                QPushButton:hover { color: #E91E63; background-color: #FDEBF0; border-radius: 20px; } 
            """)
        else:
            self.btn_like.setIcon(self.icon_grey)
            self.btn_like.setStyleSheet("""
                QPushButton { 
                    background: transparent; border: none; font-size: 16px; color: #666; padding: 8px 16px; 
                    text-align: left;
                }
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
    
    def _open_report_form(self):
        """Membuka form report untuk post ini."""
        if self.post_id is None:
            return
        
        user_model = None
        if self.post_manager and hasattr(self.post_manager, 'user_model'):
            user_model = self.post_manager.user_model
        
        if not user_model or not hasattr(user_model, 'userID') or not user_model.userID:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Peringatan", "Anda harus login untuk melaporkan post.")
            return
        
        user_id = user_model.userID
        
        if self.conn and Report:
            if Report.has_user_reported_post(self.conn, self.post_id, user_id):
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Info", "Anda sudah melaporkan post ini sebelumnya.")
                return
            
            post = PostModel.get_by_id(self.conn, self.post_id)
            if post and post.getAuthor() == user_id:
                QMessageBox.warning(self, "Peringatan", "Anda tidak dapat melaporkan post Anda sendiri.")
                return
        
        if ReportForm:
            dialog = QDialog(self)
            dialog.setWindowTitle("Laporkan Post")
            dialog.setModal(True)
            
            report_form = ReportForm(self.post_id, dialog)

            report_form.reportSubmitted.connect(
                lambda post_id, violation, details: self._handle_report_submission(post_id, violation, details, dialog)
            )
            
            layout = QVBoxLayout(dialog)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(report_form)
            
            dialog.resize(500, 400)
            dialog.exec_()
    
    def _handle_report_submission(self, post_id: int, violation_type: str, additional_details: str, dialog=None):
        """Menangani submit report dari form."""
        if not self.conn or not Report:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", "Koneksi database tidak tersedia.")
            if dialog:
                dialog.close()
            return
        
        user_model = None
        if self.post_manager and hasattr(self.post_manager, 'user_model'):
            user_model = self.post_manager.user_model
        
        if not user_model or not hasattr(user_model, 'userID') or not user_model.userID:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Peringatan", "Anda harus login untuk melaporkan post.")
            if dialog:
                dialog.close()
            return
        
        user_id = user_model.userID
        
        from PyQt5.QtCore import QDateTime
        from datetime import datetime
        
        try:
            Report.create_table(self.conn)
            time_created = datetime.now().isoformat()
            
            report = Report(
                postID=post_id,
                reporterID=user_id,
                violationType=violation_type,
                additionalDetails=additional_details,
                timeCreated=time_created,
                status="pending"
            )
            report.create_report(self.conn)
            
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Berhasil", "Laporan Anda telah dikirim. Terima kasih!")
            
            if dialog:
                dialog.accept()
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Gagal mengirim laporan: {e}")