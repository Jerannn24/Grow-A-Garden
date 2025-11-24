import sqlite3
from typing import Optional, List, Any, Tuple
import os

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(MODEL_DIR))
DB_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'app.db')

class UserModel:
    def __init__(self,
                 userID: Optional[int] = None, username: str = "", password: str = "",
                 email: str = "",
                 profileInfo: str = "",
                 role: str = "user",
                 reportCount: int = 0,
                 status: str = "active",
                 location: str = "unknown",
                 notificationPreferences: str = "all",
                 notificationTime: str = "08:00"):
        self.userID = userID
        self.username = username
        self.password = password
        self.email = email
        self.profileInfo = profileInfo
        self.role = role
        self.reportCount = reportCount
        self.status = status
        self.location = location
        self.notificationPreferences = notificationPreferences
        self.notificationTime = notificationTime
        
    @staticmethod
    def getUserID(self):
        return self.userID
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def getEmail(self):
        return self.email
    
    def getProfileInfo(self):
        return self.profileInfo
    
    def getRole(self):
        return self.role
    
    def getReportCount(self):
        return self.reportCount
    
    def getStatus(self):
        return self.status
        
    def getLocation(self):   
        return self.location
        
    def getNotificationPreferences(self):   
        return self.notificationPreferences
        
    def getNotificationTime(self): 
        return self.notificationTime 
    
    @staticmethod
    def get_conn() -> sqlite3.Connection:
        return sqlite3.connect(DB_FILE_PATH)

    
    def createTable(self, conn: sqlite3.Connection):
        """Membuat tabel users jika belum ada."""
        query = """
        CREATE TABLE IF NOT EXISTS users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            profileInfo TEXT NOT NULL DEFAULT '',
            role TEXT NOT NULL DEFAULT 'user',
            reportCount INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'active',
            location TEXT DEFAULT 'unknown',
            notificationPreferences TEXT DEFAULT 'all',
            notificationTime TEXT DEFAULT '08:00'
        )
        """
        conn.execute(query)
        conn.commit()

    def registerUser(self, username, email, password, location, confirmPassword, profileInfo=""):
        if not username or not email or not password or not confirmPassword or not location:
            return False, "Empty Field!"
        
        if password != confirmPassword:
            return False, "Password and Confirmation Password Different!"

        conn = self.get_conn()
        self.createTable(conn) 

        try:
            query = "INSERT INTO users (username, email, password, location, profileInfo) VALUES (?, ?, ?, ?, ?)"
            conn.execute(query, (username, email, password, location, profileInfo))
            conn.commit()
            return True, "Registration Sucess!"
        except sqlite3.IntegrityError:
            return False, "Username or email used!"

    def loginUser(self, email: str, password: str) -> Tuple[Optional["UserModel"], str]:
        conn = self.get_conn()
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        cursor = conn.execute(query, (email, password))
        userRow = cursor.fetchone()

        if userRow:
            userInstance = UserModel.fromRowSQL(userRow)
            if userInstance:
                userInstance.password = ""
            return userInstance, "Login Success!"
        else:
            return None, "Wrong Email or password!"

    def changePassword(self, username:str, email:str, newPassword:str, confirmPassword:str):
        if not email and not username and not newPassword and not confirmPassword:
            return False, "There Is Empty Field"
        
        print(email, username)
        
        conn = self.get_conn()
        query = "SELECT * FROM users WHERE email = ? AND username = ?"
        cursor = conn.execute(query, (email, username))
        userRow = cursor.fetchone()
        
        if not userRow:
            return False, "User not found" 

        if newPassword != confirmPassword:
            return False,"Passwords do not match" 

        update_query = "UPDATE users SET password = ? WHERE email = ? AND username = ?"
        conn.execute(update_query, (newPassword, email, username))
        conn.commit()

        return True, "Password updated successfully" 

    def updateProfil(self, userID: int, newUsername:str, newEmail: str, newProfileInfo: str, newLocation: str):
        conn = self.get_conn()

        check_query = "SELECT * FROM users WHERE userID = ?"
        cursor = conn.execute(check_query, (userID,))
        userRow = cursor.fetchone()

        if not userRow:
            return False, "User not found!"

        email_check = "SELECT userID FROM users WHERE email = ? AND userID != ?"
        cursor = conn.execute(email_check, (newEmail, userID))
        existingEmail = cursor.fetchone()

        if existingEmail:
            return False, "Email was user by another user!"

        update_query = """
            UPDATE users
            SET username = ?, email = ?, profileInfo = ?, location = ?
            WHERE userID = ?
            """
            
        conn.execute(update_query, (newUsername, newEmail, newProfileInfo, newLocation, userID))
        conn.commit()

        return True, "Profil updated!"
        
    @classmethod
    def fromRowSQL(cls, row: Tuple) -> Optional["UserModel"]:
        if row is None or len(row) < 11:
            return None
        
        try:
            return cls(
                userID=row[0], username=row[1], password=row[2], email=row[3], 
                profileInfo=row[4], role=row[5], reportCount=row[6], status=row[7], 
                location=row[8], notificationPreferences=row[9], notificationTime=row[10]
            )
        except Exception:
            return None

    @classmethod
    def getByID(cls, user_id: int) -> Optional["UserModel"]:
        conn = cls.get_conn()
        cur = conn.execute("SELECT * FROM users WHERE userID = ?", (user_id,))
        row = cur.fetchone()
        return cls.fromRowSQL(row) if row else None
