from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from models.TaskNotification import TaskNotification 

class NotificationManager(QObject):
    newNotification = pyqtSignal(int, str, str) 

    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        self.user_id = user_model.userID
        
        TaskNotification.init_table()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_notifications)
        self.timer.start(60000)
        
        self.check_notifications()

    def check_notifications(self):
        print("[DEBUG] Checking notifications...")

        # TESTING
        self.newNotification.emit(999, "Test Notification", "This is a test message.")
        pref = getattr(self.user_model, 'notificationPreferences', 'all')
        if pref != 'all':
            return

        if not self.user_id:
            return

        self._process_task_notifications()
        

    def _process_task_notifications(self):
        new_alerts = TaskNotification.generate_overdue_notifications(self.user_id)
        for alert in new_alerts:
            self.newNotification.emit(alert.get('notifID'), alert.get('title'), alert.get('content'))