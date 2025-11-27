"""
Script untuk membuat akun admin.
Jalankan script ini untuk membuat akun admin baru di database.

Usage:
    python create_admin.py
"""

import sys
import os

# Ensure the package `models` (under the project's `src` folder) is importable when
# running this script from `src/script`. The src directory is the parent of this
# script's directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # .../src/script
PROJECT_SRC = os.path.dirname(SCRIPT_DIR)  # .../src
if PROJECT_SRC not in sys.path:
    sys.path.insert(0, PROJECT_SRC)

from models.UserModel import UserModel, DB_FILE_PATH
import sqlite3

def create_admin_account():
    """Membuat akun admin baru."""
    print("=" * 50)
    print("Pembuatan Akun Admin")
    print("=" * 50)
    
    # Get admin details
    print("\nMasukkan detail akun admin:")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    location = input("Location (opsional, default: 'admin'): ").strip() or "admin"
    profile_info = input("Profile Info (opsional): ").strip()
    
    if not username or not email or not password:
        print("\n❌ Error: Username, email, dan password wajib diisi!")
        return False
    
    # Connect to database
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        conn.row_factory = sqlite3.Row
        
        # Create tables if not exist
        user_model = UserModel()
        user_model.createTable(conn)
        
        # Check if username or email already exists
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        existing = cur.fetchone()
        
        if existing:
            print(f"\n❌ Error: Username atau email sudah terdaftar!")
            conn.close()
            return False
        
        # Insert admin user
        cur.execute("""
            INSERT INTO users (username, email, password, location, profileInfo, role, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, email, password, location, profile_info, "admin", "active"))
        
        conn.commit()
        user_id = cur.lastrowid
        
        print(f"\n✅ Akun admin berhasil dibuat!")
        print(f"   User ID: {user_id}")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Role: admin")
        print("\nAnda bisa login dengan akun ini sekarang.")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    try:
        create_admin_account()
    except KeyboardInterrupt:
        print("\n\nDibatalkan oleh user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

