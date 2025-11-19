import sqlite3
from typing import Optional, List, Any, Tuple

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
    def get_conn() -> sqlite3.Connection:
        """Membuka koneksi database baru untuk operasi."""
        return sqlite3.connect('app.db')

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
            return False, "Semua field harus diisi!"
        if password != confirmPassword:
            return False, "Password dan konfirmasi password tidak cocok!"

        conn = self.get_conn()
        self.createTable(conn) 

        try:
            query = "INSERT INTO users (username, email, password, location, profileInfo) VALUES (?, ?, ?, ?, ?)"
            conn.execute(query, (username, email, password, location, profileInfo))
            conn.commit()
            return True, "Registrasi berhasil!"
        except sqlite3.IntegrityError:
            return False, "Username atau email sudah terdaftar!"

    def loginUser(self, email: str, password: str) -> Tuple[Optional["UserModel"], str]:
        conn = self.get_conn()
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        cursor = conn.execute(query, (email, password))
        user_row = cursor.fetchone()

        if user_row:
            user_instance = UserModel.fromRowSQL(user_row)
            if user_instance:
                user_instance.password = ""
            return user_instance, "Login berhasil!"
        else:
            return None, "Email atau password salah!"

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
