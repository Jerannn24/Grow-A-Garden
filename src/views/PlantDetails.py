from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor
from models.Plant import Plant
from models.Task import Task
from views.ActivityRecordPopUp import ActivityRecordPopUp
from views.PlantGrowthForm import PlantGrowthForm
import datetime

class PlantDetails(QWidget):
    backRequested = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.user_id = None
        self.plant_id = None
        
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
        self.btn_back = QPushButton("← Back to My Garden")
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

        # Setup Kartu
        self.setup_info_card()
        self.todo_card = None  
        self.content_layout.addStretch()
        scroll.setWidget(self.content_widget)
        main_layout.addWidget(scroll)

    def setup_info_card(self):
        card = QFrame()
        card.setObjectName("CardFrame")
        
        main_card_layout = QVBoxLayout(card)
        main_card_layout.setSpacing(20)
        # Urutan: Kiri, Atas, Kanan, Bawah
        main_card_layout.setContentsMargins(30, 20, 30, 30)

        # --- BAGIAN ATAS (Horizontal) --- 
        info_grid = QGridLayout()
        info_grid.setVerticalSpacing(0)    # Jarak antar baris (Atas-Bawah) jadi 0 (Rapat)
        info_grid.setHorizontalSpacing(25) # Jarak antar kolom (Icon-Teks) tetap lega
        info_grid.setContentsMargins(0, 0, 0, 0)

        # 1. ICON TANAMAN (Kiri)
        self.icon_label = QLabel("🌵") 
        self.icon_label.setFixedSize(200, 200) 
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("""
            background-color: #E8F5E9; 
            border-radius: 20px; 
            font-size: 65px; 
            padding-bottom: 5px;
        """)
        info_grid.addWidget(self.icon_label, 0, 0, 3, 1, Qt.AlignTop)

        # Baris 1: Nama
        self.lbl_name = QLabel("Loading Name...")
        self.lbl_name.setFont(QFont("Arial", 26, QFont.Bold))
        self.lbl_name.setStyleSheet("color: #212121; margin-top: -5px; margin-bottom: 0px;")
        self.lbl_name.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        info_grid.addWidget(self.lbl_name, 0, 1)

        # Baris 2: Spesies
        self.lbl_species = QLabel("Loading Species...")
        self.lbl_species.setFont(QFont("Arial", 14))
        self.lbl_species.setStyleSheet("color: #757575; margin-top: 0px; margin-bottom: 15px; font-style: italic;")
        self.lbl_species.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        info_grid.addWidget(self.lbl_species, 1, 1)

        # Baris 3: Stats (Water & Sun)
        stats_container = QHBoxLayout()
        stats_container.setSpacing(0)
        stats_container.setContentsMargins(0, 5, 0, 0) # Sedikit jarak dari spesies
        
        self.lbl_water_val = self.create_stat_pill(stats_container, "💧", "Water Frequency", "#E3F2FD", "#1565C0", 1)
        self.lbl_sun_val = self.create_stat_pill(stats_container, "☀️", "Sunlight", "#FFF8E1", "#FF8F00", 1)
        
        # Masukkan layout stats ke dalam Grid
        info_grid.addLayout(stats_container, 2, 1)

        # Masukkan Grid ke Layout Utama Kartu
        main_card_layout.addLayout(info_grid)

        # --- BAGIAN BAWAH: REKOMENDASI ---
        self.rec_box = QFrame()
        self.rec_box.setStyleSheet("background-color: #FFEBEE; border-radius: 12px; border: 1px solid #FFCDD2;")
        rec_layout = QHBoxLayout(self.rec_box)
        rec_layout.setContentsMargins(15, 12, 15, 12)
        
        self.rec_label = QLabel("⚠️ Needs watering urgently! (Placeholder Recommendation)")
        self.rec_label.setStyleSheet("color: #C62828; font-weight: bold; font-size: 14px; border: none;")
        
        rec_layout.addWidget(self.rec_label)
        main_card_layout.addWidget(self.rec_box)

        self.content_layout.addWidget(card)

    def create_stat_pill(self, parent_layout, icon, title, bg, color, stretch=0):
        pill = QFrame()
        pill.setFixedHeight(75) 
        pill.setStyleSheet(f"background-color: {bg}; border-radius: 12px;")
        
        pill_layout = QVBoxLayout(pill)
        pill_layout.setContentsMargins(15, 10, 15, 10)
        pill_layout.setSpacing(4) # Spacing antar judul dan nilai
        
        # Gunakan AlignVCenter agar konten di dalam pill juga rapi di tengah
        pill_layout.setAlignment(Qt.AlignVCenter)

        lbl_title = QLabel(f"{icon}  {title}")
        lbl_title.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
        
        lbl_val = QLabel("...")
        lbl_val.setStyleSheet("color: #333; font-size: 16px; font-weight: bold;")
        
        pill_layout.addWidget(lbl_title)
        pill_layout.addWidget(lbl_val)
        
        parent_layout.addWidget(pill, stretch)
        return lbl_val

    def setup_todo_card(self):
        if not self.user_id or not self.plant_id:
            return
        
        # Remove old todo card if it exists
        if self.todo_card is not None:
            self.content_layout.removeWidget(self.todo_card)
            self.todo_card.deleteLater()
        
        # Fetch tasks for this specific plant
        overdue_tasks = Task.getOverdueTasks(user_id=self.user_id, plant_id=self.plant_id)
        today_tasks = Task.getTodaysTodo(user_id=self.user_id, plant_id=self.plant_id)
        week_tasks = Task.getWeeksTodo(user_id=self.user_id, plant_id=self.plant_id)
        completed_tasks = Task.getCompletedTasks(user_id=self.user_id, plant_id=self.plant_id)
        
        icon_map = {
            "water": "💧",
            "fertilize": "🌱",
            "light": "☀️",
            "harvest": "🌾",
            "update": "📈"
        }

        desc_map = {
            "water": "Water your plant",
            "fertilize": "Apply fertilizer",
            "light": "Provide sunlight",
            "harvest": "Ready to harvest!",
            "update": "Log growth (height & leaf color)"
        }

        self.todo_card = QFrame()
        self.todo_card.setObjectName("CardFrame")
        layout = QVBoxLayout(self.todo_card)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Plant Tasks")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        has_tasks = False

        def add_task_section(section_title, tasks_dict, is_urgent=False):
            nonlocal has_tasks
            if not tasks_dict:
                return
            section_label = QLabel(section_title)
            section_label.setStyleSheet(
                f"font-size: 14px; font-weight: bold; color: {'#D32F2F' if is_urgent else '#2E7D32'}; margin-top: 10px;"
            )
            section_has_items = False
            for task_list in tasks_dict.values():
                for task in task_list:
                    if self._should_hide_update_task(task):
                        continue
                    if not section_has_items:
                        layout.addWidget(section_label)
                        section_has_items = True
                    icon = icon_map.get(task.actionType, "📋")
                    title_text = task.actionType.capitalize()
                    desc = desc_map.get(task.actionType, "Task")
                    self.create_task_item(
                        layout,
                        icon,
                        title_text,
                        desc,
                        is_urgent,
                        task.deadline,
                        task
                    )
                    has_tasks = True

        add_task_section("⚠️ Overdue", overdue_tasks, is_urgent=True)
        add_task_section("📅 Today", today_tasks)
        add_task_section("📆 This Week", week_tasks)

        if completed_tasks:
            section_label = QLabel("✓ Completed")
            section_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2E7D32; margin-top: 10px;")
            layout.addWidget(section_label)
            for task_list in completed_tasks.values():
                for task in task_list:
                    icon = icon_map.get(task.actionType, "📋")
                    title_text = task.actionType.capitalize()
                    desc = desc_map.get(task.actionType, "Task")
                    self.create_task_item(
                        layout,
                        icon,
                        title_text,
                        desc,
                        False,
                        task.deadline,
                        None
                    )

        if not has_tasks and not completed_tasks:
            empty_label = QLabel("No tasks for this plant. Great work! 🎉")
            empty_label.setStyleSheet("color: #999; font-size: 14px; text-align: center;")
            empty_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(empty_label)

        self.content_layout.addWidget(self.todo_card)

    def create_task_item(self, parent, icon, title, desc, is_urgent, deadline=None, task=None):
        item_frame = QFrame()
        bg = "#FFF3E0" if is_urgent else "white"
        border = "#FFCC80" if is_urgent else "#EEEEEE"
        item_frame.setStyleSheet(f"background-color: {bg}; border: 1px solid {border}; border-radius: 12px;")

        row = QHBoxLayout(item_frame)
        row.setContentsMargins(20, 15, 20, 15)
        row.setSpacing(20)
        row.setAlignment(Qt.AlignVCenter)

        lbl_icon = QLabel(icon)
        lbl_icon.setFont(QFont("Arial", 24))

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        t_color = "#D32F2F" if is_urgent else "#333"
        lbl_t = QLabel(title)
        lbl_t.setStyleSheet(f"font-weight: bold; font-size: 15px; color: {t_color}; border: none; background: transparent;")

        lbl_d = QLabel(desc)
        lbl_d.setStyleSheet("color: #666; font-size: 12px; border: none; background: transparent;")

        if deadline:
            try:
                if isinstance(deadline, datetime.datetime):
                    deadline_text = deadline.strftime("%Y-%m-%d %H:%M")
                else:
                    deadline_text = str(deadline)
            except Exception:
                deadline_text = "No deadline"
            lbl_deadline = QLabel(f"Due: {deadline_text}")
            lbl_deadline.setStyleSheet("color: #999; font-size: 11px; border: none; background: transparent; font-style: italic;")
            text_layout.addWidget(lbl_deadline)

        text_layout.addWidget(lbl_t)
        text_layout.addWidget(lbl_d)

        if task:
            btn = QPushButton("Input")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedSize(80, 38)
            btn.setStyleSheet("QPushButton { background-color: #FF6F00; color: white; border-radius: 8px; font-weight: bold; border: none; } QPushButton:hover { background-color: #E65100; }")
            btn.clicked.connect(lambda checked=False, t=task: self.show_activity_popup(t))

            row.addWidget(lbl_icon)
            row.addLayout(text_layout, 1)
            row.addWidget(btn)
        else:
            chk_label = QLabel("✓")
            chk_label.setStyleSheet("color: #2E7D32; font-size: 24px; font-weight: bold;")
            row.addWidget(lbl_icon)
            row.addLayout(text_layout, 1)
            row.addWidget(chk_label)

        parent.addWidget(item_frame)
    
    def show_activity_popup(self, task):
        """Show the activity record popup and mark task as done when confirmed"""
        if task.actionType == "update":
            popup = PlantGrowthForm(task=task, parent=self)
            popup.confirmed.connect(lambda height, color: self.on_growth_logged(task, height, color))
            popup.exec_()
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
            self.setup_todo_card()
        except Exception as e:
            print(f"❌ Error marking task as done: {e}")

    def on_growth_logged(self, task, height, color):
        try:
            Task.completeTask(task.taskID, 1)
            if self.user_id and task.plantID:
                Task.regenerateTask(self.user_id, action_type="update", plant_id=task.plantID)
            print(f"📈 Growth recorded for plant {task.plantID}: {height} cm, {color}")
            self.setup_todo_card()
        except Exception as exc:
            print(f"❌ Failed to log growth update: {exc}")

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

    def populate_data(self, plant_obj: Plant, user_id: int):
        self.user_id = user_id
        self.plant_id = plant_obj.getPlantID()
        
        water_percent = Task.getCarePercentage(plant_obj.plantID, "water")
        light_percent = Task.getCarePercentage(plant_obj.plantID, "light")
        self.lbl_name.setText(plant_obj.getPlantName())
        self.lbl_species.setText(plant_obj.getPlantSpecies())
        self.lbl_water_val.setText(f"{water_percent * 100:.1f}%")
        self.lbl_sun_val.setText(f"{light_percent * 100:.1f}%")
        
        icon = getattr(plant_obj, 'icon', '🌿') 
        self.icon_label.setText(icon)
        
        # Refresh todo card with actual user and plant data
        self.setup_todo_card()