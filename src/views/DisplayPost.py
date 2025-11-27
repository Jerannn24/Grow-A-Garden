from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QHBoxLayout, QFrame, QScrollArea, QSpacerItem, QSizePolicy, QStackedWidget, QListWidget, QListWidgetItem)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon
import os
from models.UserModel import DB_FILE_PATH

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

        # Report button (kanan atas)
        self.report_btn = QPushButton("⚠️ Report")
        self.report_btn.setCursor(Qt.PointingHandCursor)
        self.report_btn.setToolTip("Report Post")
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

        stats_row = QHBoxLayout()
        self.stats_lbl = QLabel("0 Replies   0 Retweets   0 Likes")
        self.stats_lbl.setStyleSheet("color: gray; font-size: 13px; margin-top: 10px; border: none;")
        stats_row.addWidget(self.stats_lbl)
        stats_row.addStretch()
        card_layout.addLayout(stats_row)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #EEEEEE; border: none; max-height: 1px;")
        card_layout.addWidget(line)

        actions_row = QHBoxLayout()
        actions_row.setSpacing(30)

        def create_action_btn(icon_text):
            btn = QPushButton(icon_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { background: transparent; border: none; font-size: 18px; color: #666; }
                QPushButton:hover { color: #007F00; background-color: #E8F5E9; border-radius: 15px; }
            """)
            btn.setFixedSize(40, 40)
            return btn

        self.btn_reply = create_action_btn("💬") 
        self.btn_retweet = create_action_btn("🔁") 
        self.btn_like = create_action_btn("❤️") 
        self.btn_share = create_action_btn("📤") 
        
        self.btn_delete = create_action_btn("🗑️")

        actions_row.addWidget(self.btn_reply)
        actions_row.addWidget(self.btn_retweet)
        actions_row.addWidget(self.btn_like)
        actions_row.addWidget(self.btn_share)
        actions_row.addStretch()
        actions_row.addWidget(self.btn_delete) 

        card_layout.addLayout(actions_row)

        content_layout.addWidget(self.card)
        content_layout.addStretch()
        
        scroll.setWidget(content_container)
        self.main_layout.addWidget(scroll)

        self.back_btn.clicked.connect(lambda: self.backRequested.emit())
        self.btn_like.clicked.connect(lambda: self._emit_if_set(self.likeRequested))
        self.btn_reply.clicked.connect(lambda: self._emit_if_set(self.replyRequested))
        self.btn_delete.clicked.connect(lambda: self._emit_if_set(self.deleteRequested))

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
    
    def render_post(self, post, replies_count: int = 0):
        if post is None:
            self.clear()
            return

        self.post_id = post.getPostID()
        
        from models.Post import Post as PostModel
        
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
        
        self.stats_lbl.setText(f"{replies_count} Replies • {post.getViewCount()} Views • {post.getLikeCount()} Likes")
        
        media_path = os.path.abspath(post.media)
        if media_path and os.path.isfile(media_path):
            pix = QPixmap(media_path)
            if not pix.isNull():
                scaled_pix = pix.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
            QMessageBox.warning(self, "Warning", "You need to login to report post.")
            return
        
        user_id = user_model.userID
        
        if self.conn and Report:
            if Report.has_user_reported_post(self.conn, self.post_id, user_id):
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Info", "You have reported this post before.")
                return
            
            post = PostModel.get_by_id(self.conn, self.post_id)
            if post and post.getAuthor() == user_id:
                QMessageBox.warning(self, "Warning", "You can't report your own post.")
                return
        
        if ReportForm:
            dialog = QDialog(self)
            dialog.setWindowTitle("Report Post")
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
        if not self.conn or not Report:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", "Database connection unavailable.")
            if dialog:
                dialog.close()
            return
        
        user_model = None
        if self.post_manager and hasattr(self.post_manager, 'user_model'):
            user_model = self.post_manager.user_model
        
        if not user_model or not hasattr(user_model, 'userID') or not user_model.userID:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Warning", "You need to login to report post.")
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
            QMessageBox.information(self, "Success", "Your report have been delivered. Thank you!")
            
            if dialog:
                dialog.accept()
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to deliver report: {e}")