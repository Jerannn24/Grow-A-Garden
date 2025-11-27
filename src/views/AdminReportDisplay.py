from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QListWidgetItem, QFrame,
                             QScrollArea, QMessageBox, QDialog, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont
from models.Report import Report
from models.Post import Post
from models.UserModel import UserModel
import sqlite3


class AdminReportDisplay(QWidget):
    reportSelected = pyqtSignal(int)  # reportID
    
    def __init__(self, db_path: str, conn: sqlite3.Connection, admin_user: UserModel, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.conn = conn
        self.admin_user = admin_user
        self.current_report = None
        self._init_ui()
        self.load_reports()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #007F00; padding: 15px;")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 15, 15, 15)
        
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel("📋 Report Dashboard")
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        top_row.addWidget(title_label)
        top_row.addStretch()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("background-color: rgba(255,255,255,0.12); color: white; border: 1px solid rgba(255,255,255,0.18); padding:6px 10px; border-radius:6px;")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self._manual_refresh)
        top_row.addWidget(refresh_btn)
        header_layout.addLayout(top_row)

        subtitle_label = QLabel("Manage all reports from users")
        subtitle_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 12px;")
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        list_container = QFrame()
        list_container.setStyleSheet("background-color: white;")
        list_container.setFixedWidth(400)
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)
        
        list_header = QLabel("Report List")
        list_header.setStyleSheet("""
            padding: 15px;
            background-color: #F8F9FA;
            border-bottom: 1px solid #E0E0E0;
            font-weight: bold;
            color: #333;
        """)
        list_layout.addWidget(list_header)
        
        self.report_list = QListWidget()
        self.report_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: white;
            }
            QListWidget::item {
                background-color: white;
                border-bottom: 1px solid #E0E0E0;
                padding: 15px;
                min-height: 80px;
            }
            QListWidget::item:hover {
                background-color: #F8F9FA;
            }
            QListWidget::item:selected {
                background-color: #E8F5E9;
                border-left: 4px solid #007F00;
            }
        """)
        self.report_list.itemClicked.connect(self._on_report_clicked)
        list_layout.addWidget(self.report_list)
        
        content_layout.addWidget(list_container)
        
        detail_container = QFrame()
        detail_container.setStyleSheet("background-color: #F8F9FA;")
        detail_layout = QVBoxLayout(detail_container)
        detail_layout.setContentsMargins(20, 20, 20, 20)
        detail_layout.setSpacing(15)
        
        self.detail_header = QLabel("Select report to view details")
        self.detail_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        detail_layout.addWidget(self.detail_header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_widget)
        self.detail_layout.setContentsMargins(0, 0, 0, 0)
        self.detail_layout.setSpacing(15)
        
        scroll.setWidget(self.detail_widget)
        detail_layout.addWidget(scroll)
        
        self.action_btn_container = QFrame()
        self.action_btn_container.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        action_btn_layout = QHBoxLayout(self.action_btn_container)
        action_btn_layout.setContentsMargins(0, 0, 0, 0)
        
        self.action_btn = QPushButton("⚡ Take Action")
        self.action_btn.setStyleSheet("""
            QPushButton {
                background-color: #007F00;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #006600;
            }
        """)
        self.action_btn.clicked.connect(self._open_action_form)
        self.action_btn.hide()
        action_btn_layout.addStretch()
        action_btn_layout.addWidget(self.action_btn)
        action_btn_layout.addStretch()
        
        detail_layout.addWidget(self.action_btn_container)
        
        content_layout.addWidget(detail_container, 1)
        
        layout.addLayout(content_layout)
    
    def load_reports(self):
        if not self.conn:
            return
        
        self.report_list.clear()
        reports = Report.get_all_reports_for_admin(self.conn)
        
        if not reports:
            no_report_item = QListWidgetItem("No report")
            no_report_item.setFlags(Qt.NoItemFlags)
            self.report_list.addItem(no_report_item)
            return
        
        from collections import defaultdict
        reports_by_post = defaultdict(list)
        for report in reports:
            reports_by_post[report.postID].append(report)
        
        sorted_posts = sorted(reports_by_post.items(), key=lambda x: len(x[1]), reverse=True)
        
        for post_id, post_reports in sorted_posts:
            report_count = len(post_reports)
            post = Post.get_by_id(self.conn, post_id)
            if post:
                try:
                    if getattr(post, 'isAvailable', 1) == 0:
                        post_title = "Unavailable"
                    else:
                        post_title = post.getTitle() if post.getTitle() else "(No Title)"
                except Exception:
                    post_title = post.getTitle() if post.getTitle() else "(No Title)"
            else:
                post_title = "Unavailable"
            post_content = post.getContent() if post else ""
            post_content_preview = (post_content[:50] + '...') if len(post_content) > 50 else post_content
            
            first_report = post_reports[0]
            reporter_name = Report.get_username_by_id(self.conn, first_report.reporterID)
            
            item = QListWidgetItem()
            item.setData(Qt.UserRole, first_report.reportID) 
            item.setData(Qt.UserRole + 1, post_id)  
            
            widget = QWidget()
            widget_layout = QVBoxLayout(widget)
            widget_layout.setContentsMargins(10, 10, 10, 10)
            widget_layout.setSpacing(5)
            
            count_badge = QLabel(f"🔴 {report_count} Report")
            count_badge.setStyleSheet("""
                color: #FF4444;
                font-weight: bold;
                font-size: 12px;
            """)
            widget_layout.addWidget(count_badge)
            
            title_label = QLabel(post_title)
            title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
            title_label.setWordWrap(True)
            widget_layout.addWidget(title_label)
            
            if post_content_preview:
                content_label = QLabel(post_content_preview)
                content_label.setStyleSheet("font-size: 12px; color: #666;")
                content_label.setWordWrap(True)
                widget_layout.addWidget(content_label)
            
            info_label = QLabel(f"Reporter: {reporter_name} • {first_report.violationType}")
            info_label.setStyleSheet("font-size: 11px; color: #999; margin-top: 5px;")
            widget_layout.addWidget(info_label)
            
            widget.setMinimumHeight(100)
            item.setSizeHint(QSize(380, 100))
            
            self.report_list.addItem(item)
            self.report_list.setItemWidget(item, widget)

    def _manual_refresh(self):
        try:
            self.load_reports()
        except Exception as e:
            print(f"⚠️ Failed to load reports: {e}")

        self.current_report = None
        self.action_btn.hide()
        while self.detail_layout.count():
            child = self.detail_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.detail_header.setText("Select a report to view details")
    
    def _on_report_clicked(self, item: QListWidgetItem):
        report_id = item.data(Qt.UserRole)
        if not report_id:
            return
        
        self.current_report = Report.get_by_id(self.conn, report_id)
        if not self.current_report:
            return
        
        self._show_report_detail(self.current_report)
        self.action_btn.show()
    
    def _show_report_detail(self, report: Report):
        while self.detail_layout.count():
            child = self.detail_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        post = Post.get_by_id(self.conn, report.postID)
        if not post:
            self.detail_header.setText("Post not found")
            return
        
        self.detail_header.setText("Report Details")
        
        post_frame = QFrame()
        post_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        post_layout = QVBoxLayout(post_frame)
        post_layout.setSpacing(10)
        
        post_title_label = QLabel("Post Reported:")
        post_title_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        post_layout.addWidget(post_title_label)
        
        author_name = Post.getUsernameByID(self.conn, post.getAuthor())
        author_label = QLabel(f"By: {author_name}")
        author_label.setStyleSheet("color: #666; font-size: 13px;")
        post_layout.addWidget(author_label)
        
        if post.getTitle():
            title_label = QLabel(f"Title: {post.getTitle()}")
            title_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px; margin-top: 5px;")
            title_label.setWordWrap(True)
            post_layout.addWidget(title_label)
        
        content_label = QLabel(post.getContent())
        content_label.setStyleSheet("color: #333; font-size: 13px; margin-top: 5px;")
        content_label.setWordWrap(True)
        post_layout.addWidget(content_label)
        
        self.detail_layout.addWidget(post_frame)
        
        report_frame = QFrame()
        report_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        report_layout = QVBoxLayout(report_frame)
        report_layout.setSpacing(10)
        
        report_title_label = QLabel("Report Information:")
        report_title_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        report_layout.addWidget(report_title_label)
        
        reporter_name = Report.get_username_by_id(self.conn, report.reporterID)
        reporter_label = QLabel(f"Reporter: {reporter_name}")
        reporter_label.setStyleSheet("color: #666; font-size: 13px;")
        report_layout.addWidget(reporter_label)
        
        violation_label = QLabel(f"Type of Violation: {report.violationType}")
        violation_label.setStyleSheet("color: #666; font-size: 13px;")
        report_layout.addWidget(violation_label)
        
        time_label = QLabel(f"Time: {report.timeCreated}")
        time_label.setStyleSheet("color: #666; font-size: 13px;")
        report_layout.addWidget(time_label)
        
        if report.additionalDetails:
            details_label = QLabel(f"Description: {report.additionalDetails}")
            details_label.setStyleSheet("color: #666; font-size: 13px; margin-top: 10px;")
            details_label.setWordWrap(True)
            report_layout.addWidget(details_label)
        
        report_count = Report.get_report_count_by_post(self.conn, report.postID)
        count_label = QLabel(f"Total Reports For This Post: {report_count}")
        count_label.setStyleSheet("color: #FF4444; font-weight: bold; font-size: 13px; margin-top: 10px;")
        report_layout.addWidget(count_label)
        
        self.detail_layout.addWidget(report_frame)
        
        self.detail_layout.addStretch()
    
    def _open_action_form(self):
        if not self.current_report:
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Take Action")
        dialog.setModal(True)
        
        reporter_name = Report.get_username_by_id(self.conn, self.current_report.reporterID)
        from views.AdminActionForm import AdminActionForm
        
        action_form = AdminActionForm(
            self.current_report.reportID,
            self.current_report.postID,
            reporter_name,
            self.current_report.violationType,
            dialog
        )
        action_form.actionSubmitted.connect(self._handle_admin_action)
        self._current_action_dialog = dialog

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(action_form)
        
        dialog.resize(500, 350)
        dialog.exec_()
        try:
            del self._current_action_dialog
        except Exception:
            pass
    
    def _handle_admin_action(self, report_id: int, action: str):
        if not self.conn or not self.admin_user:
            return
        
        report = Report.get_by_id(self.conn, report_id)
        if not report:
            return
        
        try:
            report.update_admin_action(self.conn, self.admin_user.userID, action)
            
            post = Post.get_by_id(self.conn, report.postID)
            if post:
                user = UserModel.getByID(post.getAuthor())
                if user:
                    try:
                        UserModel.ensure_suspended_column(self.conn)
                    except Exception:
                        pass

                    cur = self.conn.cursor()
                    info_msg = None
                    if action == "Permanent Ban":
                        ban_reason = f"{action} by {self.admin_user.username}: {report.violationType}"
                        cur.execute("UPDATE users SET status = 'banned', suspendedUntil = NULL, banReason = ? WHERE userID = ?", (ban_reason, user.userID))
                        info_msg = f"User account permanently blocked.\nReason: {ban_reason}"
                    elif action.startswith("Suspend"):
                        days = 1
                        if "3 Days" in action:
                            days = 3
                        elif "7 Days" in action:
                            days = 7
                        from datetime import datetime, timedelta
                        until_dt = (datetime.now() + timedelta(days=days))
                        until = until_dt.isoformat()
                        try:
                            friendly = until_dt.strftime("%d %b %Y %H:%M")
                        except Exception:
                            friendly = until
                        info_msg = f"User account suspended for {days} days (until {friendly})."
                        cur.execute("UPDATE users SET status = 'suspended', suspendedUntil = ? WHERE userID = ?", (until, user.userID))
                    elif action == "Delete post":
                        cur.execute("UPDATE users SET reportCount = reportCount + 1 WHERE userID = ?", (user.userID,))
                        info_msg = "Post has been deleted."
                    self.conn.commit()
                    if action != "Report Invalid":
                        try:
                            try:
                                Post.set_unavailable_by_id(self.conn, report.postID)
                                if info_msg:
                                    info_msg = info_msg + "\Related post is no longer available."
                                else:
                                    info_msg = "Related post is no longer available."
                            except Exception:
                                Post.delete_by_id(self.conn, report.postID)
                                if info_msg:
                                    info_msg = info_msg + "\Related post deleted."
                                else:
                                    info_msg = "Related post deleted."
                        except Exception as e:
                            print(f"⚠ Failed to process post {report.postID}: {e}")
                    if info_msg:
                        try:
                            parent = getattr(self, '_current_action_dialog', self)
                            QMessageBox.information(parent, "Take Action", info_msg)
                        except Exception:
                            pass
            
            self.load_reports()
            self.current_report = None
            self.action_btn.hide()
            
            while self.detail_layout.count():
                child = self.detail_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            self.detail_header.setText("Select report to view details")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to take action: {e}")

