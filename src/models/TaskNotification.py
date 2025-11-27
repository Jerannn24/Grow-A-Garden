import sqlite3
from models.UserModel import DB_FILE_PATH
from models.Task import Task 

class TaskNotification:
    def __init__(self, notifID, content, userID, sended, taskID):
        self.notifID = notifID
        self.content = content
        self.userID = userID
        self.sended = sended
        self.taskID = taskID

    @staticmethod
    def _get_conn():
        conn = sqlite3.connect(DB_FILE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def init_table():
        conn = TaskNotification._get_conn()
        query = """
        CREATE TABLE IF NOT EXISTS task_notifications (
            notifID INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            userID INTEGER,
            sended INTEGER DEFAULT 0,
            taskID INTEGER
        );
        """
        conn.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def is_exists(task_id):
        """Cek apakah notifikasi untuk taskID ini sudah pernah dibuat"""
        conn = TaskNotification._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT notifID FROM task_notifications WHERE taskID = ?", (task_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    @staticmethod
    def create(content, userID, taskID):
        """Membuat notifikasi baru"""
        conn = TaskNotification._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO task_notifications (content, userID, sended, taskID)
            VALUES (?, ?, 0, ?)
        """, (content, userID, taskID))
        
        conn.commit()
        notif_id = cursor.lastrowid
        conn.close()
        return notif_id

    @staticmethod
    def mark_as_sended(notifID):
        """Tandai notifikasi sudah tampil di layar"""
        conn = TaskNotification._get_conn()
        conn.execute("UPDATE task_notifications SET sended = 1 WHERE notifID = ?", (notifID,))
        conn.commit()
        conn.close()

    @staticmethod
    def generate_overdue_notifications(user_id):
        """
        1. Mengambil task overdue dari Model Task.
        2. Mengecek apakah sudah ada di tabel notifikasi.
        3. Jika belum, insert ke DB.
        4. Mengembalikan list notifikasi BARU (untuk ditampilkan popup).
        """
        new_notifications_to_show = []
        
        overdue_groups = Task.getOverdueTasks(user_id)
        
        for plant_id, task_list in overdue_groups.items():
            for task in task_list:
                
                if TaskNotification.is_exists(task.taskID):
                    continue
                
                title = "Task Overdue!"
                content = f"Reminder: Action '{task.actionType}' needs to be done."
                
                notif_id = TaskNotification.create(content, user_id, task.taskID)
                
                new_notifications_to_show.append({
                    'notifID': notif_id,
                    'title': title,
                    'content': content
                })
                
                print(f"[TaskNotification] Generated new alert for Task {task.taskID}")
                
        return new_notifications_to_show