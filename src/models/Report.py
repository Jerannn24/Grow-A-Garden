import sqlite3
from typing import Optional, List, Any, Tuple
from datetime import datetime
from models.UserModel import DB_FILE_PATH


class Report:
    VIOLATION_TYPES = [
        "Spam",
        "Misinformasi",
        "Konten Tidak Pantas",
        "Ujaran Kebencian",
        "Pelanggaran Hak Cipta",
        "Lainnya"
    ]
    
    ADMIN_ACTIONS = [
        "Laporan Tidak Valid",
        "Berikan Peringatan",
        "Suspend 1 Hari",
        "Suspend 3 Hari",
        "Suspend 7 Hari",
        "Ban Permanen"
    ]
    
    def __init__(self,
                 reportID: Optional[int] = None,
                 postID: int = 0,
                 reporterID: int = 0,
                 violationType: str = "",
                 additionalDetails: str = "",
                 timeCreated: str = "",
                 status: str = "pending",
                 adminAction: str = "",
                 adminID: Optional[int] = None,
                 actionTime: Optional[str] = None):
        self.reportID = reportID
        self.postID = postID
        self.reporterID = reporterID
        self.violationType = violationType
        self.additionalDetails = additionalDetails
        self.timeCreated = timeCreated
        self.status = status  
        self.adminAction = adminAction
        self.adminID = adminID
        self.actionTime = actionTime

    @staticmethod
    def get_conn() -> sqlite3.Connection:
        """Membuka koneksi database baru untuk operasi."""
        return sqlite3.connect(DB_FILE_PATH)

    @classmethod
    def create_table(cls, conn: sqlite3.Connection):
        """Membuat tabel reports jika belum ada."""
        query = """
        CREATE TABLE IF NOT EXISTS reports (
            reportID INTEGER PRIMARY KEY AUTOINCREMENT,
            postID INTEGER NOT NULL,
            reporterID INTEGER NOT NULL,
            violationType TEXT NOT NULL,
            additionalDetails TEXT DEFAULT '',
            timeCreated TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            adminAction TEXT DEFAULT '',
            adminID INTEGER,
            actionTime TEXT,
            FOREIGN KEY (postID) REFERENCES postList(postID),
            FOREIGN KEY (reporterID) REFERENCES users(userID),
            FOREIGN KEY (adminID) REFERENCES users(userID)
        )
        """
        conn.execute(query)
        conn.commit()

    def create_report(self, conn: sqlite3.Connection):
        """Menyimpan report baru ke database."""
        Report.create_table(conn)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reports (postID, reporterID, violationType, additionalDetails, timeCreated, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.postID, self.reporterID, self.violationType, 
              self.additionalDetails, self.timeCreated, self.status))
        conn.commit()
        self.reportID = cur.lastrowid

    @classmethod
    def fromRowSQL(cls, row: Any) -> Optional["Report"]:
        """Membuat instance Report dari baris SQL."""
        if row is None:
            return None
        
        try:
            if isinstance(row, sqlite3.Row):

                def _get(column, default=None):
                    return row[column] if column in row.keys() and row[column] is not None else default

                return cls(
                    reportID=row["reportID"],
                    postID=row["postID"],
                    reporterID=row["reporterID"],
                    violationType=row["violationType"],
                    additionalDetails=_get("additionalDetails", ""),
                    timeCreated=row["timeCreated"],
                    status=_get("status", "pending"),
                    adminAction=_get("adminAction", ""),
                    adminID=_get("adminID"),
                    actionTime=_get("actionTime")
                )
            else:
                # Handle tuple format
                return cls(
                    reportID=row[0],
                    postID=row[1],
                    reporterID=row[2],
                    violationType=row[3],
                    additionalDetails=row[4] if len(row) > 4 else "",
                    timeCreated=row[5] if len(row) > 5 else "",
                    status=row[6] if len(row) > 6 else "pending",
                    adminAction=row[7] if len(row) > 7 else "",
                    adminID=row[8] if len(row) > 8 else None,
                    actionTime=row[9] if len(row) > 9 else None
                )
        except Exception as e:
            print(f"⚠️ Error creating Report from row: {e}")
            return None

    @classmethod
    def get_by_id(cls, conn: sqlite3.Connection, report_id: int) -> Optional["Report"]:
        """Mendapatkan report berdasarkan ID."""
        if conn is None:
            return None
        cur = conn.execute("SELECT * FROM reports WHERE reportID = ?", (report_id,))
        row = cur.fetchone()
        return cls.fromRowSQL(row) if row else None

    @classmethod
    def get_all_reports_for_admin(cls, conn: sqlite3.Connection) -> List["Report"]:
        """Mendapatkan semua report untuk admin dengan sorting:
        1. Prioritas: report terbanyak per post
        2. Prioritas kedua: report paling lama ke paling baru
        """
        if conn is None:
            return []
        

        query = """
        SELECT r.*, COUNT(r2.reportID) as report_count
        FROM reports r
        LEFT JOIN reports r2 ON r.postID = r2.postID AND r2.status = 'pending'
        WHERE r.status = 'pending'
        GROUP BY r.reportID
        ORDER BY report_count DESC, r.timeCreated ASC
        """
        
        cur = conn.execute(query)
        rows = cur.fetchall()
        reports = []
        for row in rows:
            report = cls.fromRowSQL(row)
            if report:
                reports.append(report)
        return reports

    @classmethod
    def get_reports_by_post(cls, conn: sqlite3.Connection, post_id: int) -> List["Report"]:
        """Mendapatkan semua report untuk post tertentu."""
        if conn is None:
            return []
        cur = conn.execute("SELECT * FROM reports WHERE postID = ?", (post_id,))
        rows = cur.fetchall()
        return [cls.fromRowSQL(row) for row in rows if cls.fromRowSQL(row) is not None]

    @classmethod
    def get_report_count_by_post(cls, conn: sqlite3.Connection, post_id: int) -> int:
        """Menghitung jumlah report untuk post tertentu."""
        if conn is None:
            return 0
        cur = conn.execute("SELECT COUNT(*) FROM reports WHERE postID = ? AND status = 'pending'", (post_id,))
        row = cur.fetchone()
        return int(row[0]) if row else 0

    @classmethod
    def has_user_reported_post(cls, conn: sqlite3.Connection, post_id: int, user_id: int) -> bool:
        """Cek apakah user sudah pernah report post ini."""
        if conn is None:
            return False
        cur = conn.execute("SELECT 1 FROM reports WHERE postID = ? AND reporterID = ? LIMIT 1", 
                          (post_id, user_id))
        return cur.fetchone() is not None

    def update_admin_action(self, conn: sqlite3.Connection, admin_id: int, action: str):
        """Update report dengan aksi admin."""
        if conn is None or self.reportID is None:
            return
        
        self.adminAction = action
        self.adminID = admin_id
        self.actionTime = datetime.now().isoformat()
        
        if action == "Laporan Tidak Valid":
            self.status = "dismissed"
        else:
            self.status = "action_taken"
        
        cur = conn.cursor()
        cur.execute("""
            UPDATE reports 
            SET adminAction = ?, adminID = ?, actionTime = ?, status = ?
            WHERE reportID = ?
        """, (self.adminAction, self.adminID, self.actionTime, self.status, self.reportID))
        conn.commit()
        
        if self.status == "action_taken":
            cur.execute("""
                UPDATE reports 
                SET status = 'reviewed'
                WHERE postID = ? AND status = 'pending' AND reportID != ?
            """, (self.postID, self.reportID))
            conn.commit()

    @staticmethod
    def get_username_by_id(conn: sqlite3.Connection, user_id: int) -> str:
        """Mendapatkan username berdasarkan userID."""
        if conn is None:
            return f"User {user_id}"
        try:
            cur = conn.execute("SELECT username FROM users WHERE userID = ?", (user_id,))
            row = cur.fetchone()
            if row:
                return row[0] if isinstance(row, tuple) else row['username']
            return f"User {user_id}"
        except Exception as e:
            print(f"⚠️ Error getting username for userID {user_id}: {e}")
            return f"User {user_id}"

