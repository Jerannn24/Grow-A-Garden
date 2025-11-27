import sqlite3
from typing import Optional, List, Any, Tuple
import os
from datetime import datetime 
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(MODEL_DIR))
DB_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'app.db')
GUIDE_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'plants.db')

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
                 notificationTime: str = "08:00",
                 timeCreated: Optional[str] = None):
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
        if timeCreated is None:
            self.timeCreated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.timeCreated = timeCreated
            
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
    
    def getTimeCreated(self):
        return self.timeCreated
    
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
            notificationTime TEXT DEFAULT '08:00',
            timeCreated TEXT DEFAULT CURRENT_TIMESTAMP -- timeCreated added
        )
        """
        conn.execute(query)
        conn.commit()

    def registerUser(self, username, email, password, location, confirmPassword, profileInfo=""):
        MIN_PASSWORD_LENGTH = 8
        
        if not username or not email or not password or not confirmPassword or not location:
            return False, "Empty Field!"
        
        if password != confirmPassword:
            return False, "Password and Confirmation Password Different!"

        if len(password) < MIN_PASSWORD_LENGTH:
            return False, f"Password is too short! It must be at least {MIN_PASSWORD_LENGTH} characters long."
            
        conn = self.get_conn()
        self.createTable(conn) 

        try:
            query = "INSERT INTO users (username, email, password, location, profileInfo, timeCreated) VALUES (?, ?, ?, ?, ?, ?)"
            conn.execute(query, (username, email, password, location, profileInfo, self.timeCreated))
            conn.commit()
            return True, "Registration Success!"
        except sqlite3.IntegrityError:
            return False, "Username or Email already exists!"
        finally:
            conn.close()

    def loginUser(self, email: str, password: str) -> Tuple[Optional["UserModel"], str]:
        conn = self.get_conn()
        try:
            query = "SELECT * FROM users WHERE email = ? AND password = ?"
            cursor = conn.execute(query, (email, password))
            user_row = cursor.fetchone()

            if not user_row:
                return None, "Email or password incorrect!"

            user_instance = UserModel.fromRowSQL(user_row)
            if not user_instance:
                return None, "Email or password incorrect!"

            from datetime import datetime
            suspended_until = getattr(user_instance, 'suspendedUntil', None)
            ban_reason = getattr(user_instance, 'banReason', '')
            try:
                cur = conn.cursor()
                cur.execute("SELECT suspendedUntil, banReason FROM users WHERE userID = ?", (user_instance.userID,))
                r = cur.fetchone()
                if r:
                    suspended_until = r[0] if isinstance(r, tuple) else (r['suspendedUntil'] if 'suspendedUntil' in r.keys() else suspended_until)
                    ban_reason = r[1] if isinstance(r, tuple) else (r['banReason'] if 'banReason' in r.keys() else ban_reason)
            except Exception:
                pass

            if user_instance.status == 'banned':
                msg = "Account Permanently Banned."
                if ban_reason:
                    msg += f" Reason: {ban_reason}"
                return None, msg

            if user_instance.status == 'suspended':
                if suspended_until:
                    try:
                        dt = datetime.fromisoformat(suspended_until)
                        now = datetime.now()
                        if dt > now:
                            delta = dt - now
                            days = delta.days
                            hours = delta.seconds // 3600
                            minutes = (delta.seconds % 3600) // 60
                            parts = []
                            if days:
                                parts.append(f"{days} days")
                            if hours:
                                parts.append(f"{hours} hours")
                            if minutes:
                                parts.append(f"{minutes} minutes")
                            remaining = ", ".join(parts) if parts else "a few seconds"
                            try:
                                friendly = dt.strftime("%d %b %Y %H:%M")
                            except Exception:
                                friendly = suspended_until
                            return None, f"Account Suspended. Remaining suspension time: {remaining} (until {friendly})."
                        else:
                            conn2 = self.get_conn()
                            try:
                                conn2.execute("UPDATE users SET status = 'active', suspendedUntil = NULL WHERE userID = ?", (user_instance.userID,))
                                conn2.commit()
                            finally:
                                conn2.close()
                            user_instance.status = 'active'
                            user_instance.suspendedUntil = None
                    except Exception:
                        return None, "Account Suspended."
                else:
                    return None, "Account Suspended."

            user_instance.password = ""
            return user_instance, "Login Success!"
        finally:
            conn.close()

    def changePassword(self, username:str, email:str, newPassword:str, confirmPassword:str):
        if not email and not username and not newPassword and not confirmPassword:
            return False, "There Is Empty Field"
        
        if len(newPassword) < 8:
            return None, f"Password is too short! It must be at least 8 characters long."
        
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

    def updateProfil(self, userID: int, newUsername:str, newEmail: str, newLocation: str, newProfileInfo: str,):
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
        if row is None:
            return None
        
        try:
            if isinstance(row, sqlite3.Row):
                suspended = row['suspendedUntil'] if 'suspendedUntil' in row.keys() else None
                ban_reason = row['banReason'] if 'banReason' in row.keys() else ''
                inst = cls(
                    userID=row['userID'], username=row['username'], password=row['password'], email=row['email'],
                    profileInfo=row['profileInfo'], role=row['role'], reportCount=row['reportCount'], status=row['status'],
                    location=row['location'], notificationPreferences=row['notificationPreferences'], notificationTime=row['notificationTime']
                )
                inst.suspendedUntil = suspended
                inst.banReason = ban_reason
                return inst
            else:
                suspended = None
                if len(row) >= 13:
                    suspended = row[8]
                    ban_reason = row[9]
                    location = row[10] if len(row) > 10 else 'unknown'
                    notificationPreferences = row[11] if len(row) > 11 else 'all'
                    notificationTime = row[12] if len(row) > 12 else '08:00'
                    inst = cls(
                        userID=row[0], username=row[1], password=row[2], email=row[3],
                        profileInfo=row[4], role=row[5], reportCount=row[6], status=row[7],
                        location=location, notificationPreferences=notificationPreferences, notificationTime=notificationTime
                    )
                    inst.suspendedUntil = suspended
                    inst.banReason = ban_reason
                    return inst
                else:
                    inst = cls(
                        userID=row[0], username=row[1], password=row[2], email=row[3],
                        profileInfo=row[4], role=row[5], reportCount=row[6], status=row[7],
                        location=row[8], notificationPreferences=row[9], notificationTime=row[10]
                    )
                    inst.suspendedUntil = None
                    inst.banReason = ''
                    return inst
        except Exception:
            return None

    @classmethod
    def getByID(cls, user_id: int) -> Optional["UserModel"]:
        conn = cls.get_conn()
        try:
            cur = conn.execute("SELECT * FROM users WHERE userID = ?", (user_id,))
            row = cur.fetchone()
            return cls.fromRowSQL(row) if row else None
        finally:
            conn.close()
