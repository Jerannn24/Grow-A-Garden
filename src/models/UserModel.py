import sqlite3

class UserModel:
    def __init__(self):
        self.conn = sqlite3.connect('app.db')
        self.createTable()
        self.currentUser = None  # session user

    def createTable(self):
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
        self.conn.execute(query)
        self.conn.commit()

    def registerUser(self, username, email, password, location, confirmPassword, profileInfo=""):
        # validasi sederhana
        if not username or not email or not password or not confirmPassword or not location:
            return False, "Semua field harus diisi!"

        if password != confirmPassword:
            return False, "Password dan konfirmasi password tidak cocok!"

        try:
            query = "INSERT INTO users (username, email, password, location, profileInfo) VALUES (?, ?, ?, ?, ?)"
            self.conn.execute(query, (username, email, password, location, profileInfo))
            self.conn.commit()
            return True, "Registrasi berhasil!"
        except sqlite3.IntegrityError:
            return False, "Username atau email sudah terdaftar!"

    def loginUser(self, email, password):
        query = """
        SELECT userID, username, email, profileInfo, role, reportCount, status, location,
            notificationPreferences, notificationTime
        FROM users
        WHERE email = ? AND password = ?
        """
        cursor = self.conn.execute(query, (email, password))
        user = cursor.fetchone()
        
        if user:
            # simpan semua properti di session
            self.currentUser = {
                "userID": user[0],
                "username": user[1],
                "email": user[2],
                "profileInfo": user[3],
                "role": user[4],
                "reportCount": user[5],
                "status": user[6],
                "location": user[7],
                "notificationPreferences": user[8],
                "notificationTime": user[9]
            }
            return True, "Login berhasil!"
        else:
            return False, "Username atau password salah!"

    def getAllUsers(self):
        cursor = self.conn.execute("SELECT userID, username, email FROM users")
        return cursor.fetchall()

    def getCurrentUser(self):
        return self.currentUser

    def logoutUser(self):
        self.currentUser = None

    def updateProfile(self, userID, profileInfo=None, location=None,
                          notificationPreferences=None, notificationTime=None):
        updates = []
        params = []

        if profileInfo is not None:
            updates.append("profileInfo = ?")
            params.append(profileInfo)
        if location is not None:
            updates.append("location = ?")
            params.append(location)
        if notificationPreferences is not None:
            updates.append("notificationPreferences = ?")
            params.append(notificationPreferences)
        if notificationTime is not None:
            updates.append("notificationTime = ?")
            params.append(notificationTime)

        if not updates:
            return False, "Tidak ada data yang diupdate!"

        params.append(userID)
        query = f"UPDATE users SET {', '.join(updates)} WHERE userID = ?"
        self.currentUser["profileInfo"] = profileInfo if profileInfo is not None else self.currentUser.get('profileInfo')
        self.currentUser["location"] = location if location is not None else self.currentUser.get('location')
        self.currentUser["notificationPreferences"] = notificationPreferences if notificationPreferences is not None else self.currentUser.get('notificationPreferences')
        self.currentUser["notificationTime"] = notificationTime if notificationTime is not None else self.currentUser.get('notificationTime')
        self.conn.execute(query, params)
        self.conn.commit()
        return True, "Profil berhasil diperbarui!"
    
    def changePassword(self, username, email, newPassword, confirmNewPassword):
        if newPassword != confirmNewPassword:
            return False, "Password dan konfirmasi password tidak cocok!"

        query = "UPDATE users SET password = ? WHERE username = ? AND email = ?"
        cursor = self.conn.execute(query, (newPassword, username, email))
        self.conn.commit()

        if cursor.rowcount == 0:
            return False, "username atau email tidak valid!"
        
        return True, "Password berhasil diubah!"
