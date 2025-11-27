from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from views.DisplayToDoList import DisplayToDoList
from models.Task import Task
from models.UserModel import UserModel


class ToDoListManager(QWidget):
    """
    Controller that manages the ToDoList display and interactions.
    Connects DisplayToDoList UI with Task model and application flow.
    """
    
    # Signals
    backRequested = pyqtSignal()
    taskInputRequested = pyqtSignal(int, int)  # Emits (user_id, task_id)
    
    def __init__(self, current_user: UserModel = None, parent=None):
        super().__init__(parent)
        
        self.current_user = current_user
        self.task_list_view = DisplayToDoList()
        
        # Connect UI signals
        self.task_list_view.backRequested.connect(self._on_back_requested)
        
        # Setup layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.task_list_view)
        
        self.setLayout(layout)
    
    def set_current_user(self, user_model: UserModel):
        """Set the current user and reload tasks"""
        self.current_user = user_model
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """Refresh the task list for the current user"""
        if not self.current_user:
            return
        
        user_id = self.current_user.getUserID()
        self.task_list_view.populate_tasks(user_id)
    
    def _on_back_requested(self):
        """Handle back button pressed"""
        self.backRequested.emit()
    
    def get_task_by_id(self, task_id):
        """Retrieve a specific task by ID"""
        try:
            conn = Task.getConnectionApp()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                from models.Task import Task as TaskModel
                return TaskModel(
                    taskID=row['task_id'],
                    plantID=row['plant_id'],
                    actionType=row['action_type'],
                    quantity=row['quantity'],
                    status=bool(row['status']),
                    deadline=row['deadline']
                )
            return None
        except Exception as e:
            print(f"Error fetching task: {e}")
            return None
    
    def mark_task_complete(self, task_id):
        """Mark a task as complete"""
        try:
            conn = Task.getConnectionApp()
            cursor = conn.cursor()
            
            from datetime import datetime
            cursor.execute("""
                UPDATE tasks
                SET status = 1, time_done = ?, actual_quantity = 1
                WHERE task_id = ?
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_id))
            
            conn.commit()
            conn.close()
            
            # Refresh the list
            self.refresh_tasks()
            return True
        except Exception as e:
            print(f"Error marking task complete: {e}")
            return False
    
    def delete_task(self, task_id):
        """Delete a task"""
        try:
            conn = Task.getConnectionApp()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            conn.commit()
            conn.close()
            
            # Refresh the list
            self.refresh_tasks()
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
    
    def regenerate_tasks_for_user(self, action_type=None):
        """Regenerate tasks for the current user"""
        if not self.current_user:
            return False
        
        try:
            user_id = self.current_user.getUserID()
            Task.regenerateTask(user_id, action_type=action_type)
            self.refresh_tasks()
            return True
        except Exception as e:
            print(f"Error regenerating tasks: {e}")
            return False
