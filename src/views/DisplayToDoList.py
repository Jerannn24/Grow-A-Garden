from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor
from models.Task import Task
from models.Plant import Plant
from views.ActivityRecordPopUp import ActivityRecordPopUp
from views.PlantGrowthForm import PlantGrowthForm
import datetime

class DisplayToDoList(QWidget):
    backRequested = pyqtSignal()
    taskInputRequested = pyqtSignal(int)  # Emits task_id

    def __init__(self):
        super().__init__()
        
        self.user_id = None
        self.task_mapping = {}  # Maps button objects to task IDs
        
        self.setStyleSheet("""
            QWidget { background-color: #F8F9FA; }
            .QFrame#CardFrame { background-color: white; border-radius: 16px; border: 1px solid #E0E0E0; }
            .QLabel#SectionTitle { font-size: 20px; font-weight: bold; color: #2E2E2E; }
        """)
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 0, 30, 30)
        main_layout.setSpacing(15)

        # Tombol Back
        btn_container = QHBoxLayout()
        self.btn_back = QPushButton("← Back")
        self.btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_back.setStyleSheet("""
            QPushButton { border: none; color: #2E7D32; font-size: 16px; font-weight: bold; text-align: left; background: transparent; }
            QPushButton:hover { color: #1B5E20; }
        """)
        self.btn_back.clicked.connect(self.backRequested.emit)
        btn_container.addWidget(self.btn_back)
        btn_container.addStretch()
        main_layout.addLayout(btn_container)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(25)
        self.content_layout.setContentsMargins(0, 10, 0, 20)

        # Placeholder for task sections
        self.content_layout.addStretch()
        scroll.setWidget(self.content_widget)
        main_layout.addWidget(scroll)

    def populate_tasks(self, user_id: int):
        """Load and display all tasks for the given user, grouped by category"""
        self.user_id = user_id
        print(f"[DEBUG-UI] populate_tasks called with user_id={user_id}")
        
        # Clear existing sections (keep the last stretch)
        while self.content_layout.count() > 1:
            item = self.content_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        # Fetch incomplete tasks
        overdue_tasks = Task.getOverdueTasks(user_id)
        today_tasks = Task.getTodaysTodo(user_id)
        week_tasks = Task.getWeeksTodo(user_id)
        
        # Fetch completed tasks
        completed_tasks = Task.getCompletedTasks(user_id)
        
        print(f"[DEBUG-UI] Tasks fetched - overdue: {len(overdue_tasks)}, today: {len(today_tasks)}, week: {len(week_tasks)}, completed: {len(completed_tasks)}")
        
        # Create section cards
        if overdue_tasks:
            self.create_task_section("Pending (Overdue)", overdue_tasks, is_urgent=True)
        
        if today_tasks:
            self.create_task_section("Today", today_tasks, is_urgent=False)
        
        if week_tasks:
            self.create_task_section("This Week", week_tasks, is_urgent=False)
        
        # Show completed tasks at the bottom
        if completed_tasks:
            self.create_task_section("Completed", completed_tasks, is_urgent=False, completed=True)
        
        # If no incomplete tasks at all
        if not overdue_tasks and not today_tasks and not week_tasks:
            if not completed_tasks:
                empty_label = QLabel("No tasks for you right now. Well done! 🎉")
            else:
                empty_label = QLabel("All tasks completed! 🎉")
            empty_label.setStyleSheet("color: #999; font-size: 14px; text-align: center;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.content_layout.insertWidget(0, empty_label)
        
        # Add stretch at the end
        self.content_layout.addStretch()

    def create_task_section(self, section_title: str, tasks_dict: dict, is_urgent: bool = False, completed: bool = False):
        """Create a card section containing task items grouped by plant"""
        card = QFrame()
        card.setObjectName("CardFrame")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Section title
        title = QLabel(section_title)
        title.setObjectName("SectionTitle")
        if is_urgent:
            title.setStyleSheet("font-size: 20px; font-weight: bold; color: #D32F2F;")
        elif completed:
            title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2E7D32;")
        layout.addWidget(title)
        
        # Icon map for action types
        icon_map = {
            "water": "💧",
            "fertilize": "🌱",
            "light": "☀️",
            "harvest": "🌾",
            "update": "📈"
        }
        
        # Description map
        desc_map = {
            "water": "Water your plant",
            "fertilize": "Apply fertilizer",
            "light": "Provide sunlight",
            "harvest": "Ready to harvest!",
            "update": "Log growth (height & leaf color)"
        }
        
        # Group tasks by plant and add them
        for plant_id, task_list in sorted(tasks_dict.items()):
            # Get plant name
            plant_name = Plant.getPlantNameByID(plant_id)
            for task in sorted(task_list, key=lambda t: t.deadline):
                if self._should_hide_update_task(task):
                    continue
                icon = icon_map.get(task.actionType, "📋")
                title_text = task.actionType.capitalize()
                desc = desc_map.get(task.actionType, "Task")
                
                # Check if task is overdue
                task_is_urgent = not task.status and task.deadline < datetime.datetime.now()
                
                self.create_task_item(
                    layout,
                    icon,
                    f"{title_text} - {plant_name}",
                    desc,
                    task_is_urgent,
                    task.deadline,
                    task if not completed else None  # Don't pass task for completed tasks (no Input button)
                )
        
        self.content_layout.insertWidget(self.content_layout.count() - 1, card)

    def create_task_item(self, parent_layout, icon, title, desc, is_urgent, deadline, task=None):
        """Create an individual task item card"""
        item_frame = QFrame()
        bg = "#FFF3E0" if is_urgent else "white"
        border = "#FFCC80" if is_urgent else "#EEEEEE"
        item_frame.setStyleSheet(f"background-color: {bg}; border: 1px solid {border}; border-radius: 12px;")
        
        row = QHBoxLayout(item_frame)
        row.setContentsMargins(20, 15, 20, 15)
        row.setSpacing(20)
        row.setAlignment(Qt.AlignVCenter)
        
        # Icon
        lbl_icon = QLabel(icon)
        lbl_icon.setFont(QFont("Arial", 24))
        
        # Text layout (title, description, deadline)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        t_color = "#D32F2F" if is_urgent else "#333"
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"font-weight: bold; font-size: 15px; color: {t_color}; border: none; background: transparent;")
        
        lbl_desc = QLabel(desc)
        lbl_desc.setStyleSheet("color: #666; font-size: 12px; border: none; background: transparent;")
        
        # Format deadline safely
        try:
            if isinstance(deadline, datetime.datetime):
                deadline_str = deadline.strftime("%Y-%m-%d %H:%M")
            else:
                deadline_str = str(deadline)
        except:
            deadline_str = "No deadline"
        lbl_deadline = QLabel(f"Due: {deadline_str}")
        lbl_deadline.setStyleSheet("color: #999; font-size: 11px; border: none; background: transparent; font-style: italic;")
        
        text_layout.addWidget(lbl_title)
        text_layout.addWidget(lbl_desc)
        text_layout.addWidget(lbl_deadline)
        
        # Input button (only for incomplete tasks)
        if task:
            btn = QPushButton("Input")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedSize(80, 38)
            btn.setStyleSheet("QPushButton { background-color: #FF6F00; color: white; border-radius: 8px; font-weight: bold; border: none; } QPushButton:hover { background-color: #E65100; }")
            
            # Connect button to show popup
            btn.clicked.connect(lambda checked=False, t=task: self.show_activity_popup(t))
            
            row.addWidget(lbl_icon)
            row.addLayout(text_layout, 1)
            row.addWidget(btn)
        else:
            # For completed tasks, show checkmark and actual quantity
            chk_label = QLabel("✓")
            chk_label.setStyleSheet("color: #2E7D32; font-size: 24px; font-weight: bold;")
            
            row.addWidget(lbl_icon)
            row.addLayout(text_layout, 1)
            row.addWidget(chk_label)
        
        parent_layout.addWidget(item_frame)
    
    def show_activity_popup(self, task):
        """Show the activity record popup and mark task as done when confirmed"""
        if task.actionType == "update":
            self.show_growth_form(task)
            return

        popup = ActivityRecordPopUp(task=task, parent=self)
        popup.confirmed.connect(lambda qty: self.on_task_confirmed(task, qty))
        popup.exec_()
    
    def on_task_confirmed(self, task, quantity):
        """Mark the task as done when user confirms activity"""
        try:
            # Update task as completed with actual quantity
            Task.completeTask(task.taskID, quantity)
            print(f"✅ Task {task.taskID} marked as done with quantity {quantity}")
            # Refresh the task display
            self.populate_tasks(self.user_id)
        except Exception as e:
            print(f"❌ Error marking task as done: {e}")

    def show_growth_form(self, task):
        popup = PlantGrowthForm(task=task, parent=self)
        popup.confirmed.connect(lambda height, color: self.on_growth_logged(task, height, color))
        popup.exec_()

    def on_growth_logged(self, task, height, color):
        try:
            Task.completeTask(task.taskID, 1)
            if self.user_id:
                Task.regenerateTask(self.user_id, action_type="update", plant_id=task.plantID)
            print(f"📈 Growth recorded for plant {task.plantID}: {height} cm, {color}")
            self.populate_tasks(self.user_id)
        except Exception as exc:
            print(f"❌ Failed to finalize growth update: {exc}")

    def _should_hide_update_task(self, task):
        if task is None or task.actionType != "update":
            return False
        deadline = task.deadline
        if not deadline:
            return False
        try:
            if not isinstance(deadline, datetime.datetime):
                deadline = datetime.datetime.fromisoformat(str(deadline))
        except Exception:
            return False
        return deadline - datetime.datetime.now() > datetime.timedelta(days=7)
