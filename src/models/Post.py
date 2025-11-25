import sqlite3
from typing import Optional, List, Any, Tuple

class Post:
    def __init__(self, postID: Optional[int]=None, userID: Optional[int]=None, repliedPostID: Optional[int]=None,
                 title: str = "", content: str = "", media: str = "", timeCreated: str = "", viewCount: int = 0,
                 likeCount: int = 0, isAvailable: int = 1):
        self.postID = postID
        self.userID = userID
        self.repliedPostID = repliedPostID
        self.title = title
        self.content = content
        self.media = media
        self.timeCreated = timeCreated
        self.viewCount = viewCount
        self.likeCount = likeCount
        self.isAvailable = isAvailable

    def getPostID(self) -> Optional[int]:
        return self.postID

    def getAuthor(self) -> Optional[int]:
        return self.userID

    def getTitle(self) -> str:
        return self.title

    def getContent(self) -> str:
        return self.content

    def setTitle(self, title: str):
        self.title = title

    def setContent(self, content: str):
        self.content = content

    def getLikeCount(self) -> int:
        return self.likeCount

    def getViewCount(self) -> int:
        return self.viewCount

    def setLikeCount(self, likeCount: int):
        self.likeCount = likeCount

    def setViewCount(self, viewCount: int):
        self.viewCount = viewCount

    def toTuple(self) -> Tuple[Any, ...]:
        return (self.userID, self.repliedPostID, self.title, self.content, self.media,
                self.timeCreated, self.viewCount, self.likeCount)
    
    @classmethod
    def fromRowSQL(cls, row: Any) -> Optional["Post"]:
        if row is None:
            return None

        try:
            def _get(key, default=None):
                try:

                    return row[key] if key in row.keys() and row[key] is not None else default
                except Exception:
                    return default

            return cls(postID=row["postID"],
                       userID=row["userID"],
                       repliedPostID=row["repliedPostID"],
                       title=row["title"],
                       content=row["content"],
                       media=row["media"],
                       timeCreated=row["timeCreated"],
                       viewCount=row["viewCount"],
                       likeCount=row["likeCount"],
                       isAvailable=_get("isAvailable", 1))
        except Exception:
            try:
                isAvail = row[9] if len(row) > 9 else 1
                return cls(postID=row[0],
                           userID=row[1],
                           repliedPostID=row[2],
                           title=row[3],
                           content=row[4],
                           media=row[5],
                           timeCreated=row[6],
                           viewCount=row[7],
                           likeCount=row[8],
                           isAvailable=isAvail)
            except Exception:
                return None

    @classmethod
    def create_table(cls, conn: sqlite3.Connection):
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS postList (
          postID INTEGER PRIMARY KEY AUTOINCREMENT,
          userID INTEGER,
          repliedPostID INTEGER,
          title TEXT,
          content TEXT,
          media TEXT,
          timeCreated TEXT,
                    viewCount INTEGER DEFAULT 0,
                    likeCount INTEGER DEFAULT 0,
                    isAvailable INTEGER DEFAULT 1
        );
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS postLikes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          postID INTEGER,
          userID INTEGER,
          UNIQUE(postID, userID)
        );
        """)
        conn.commit()

    @classmethod
    def ensure_availability_column(cls, conn: sqlite3.Connection):
        """Ensure the `isAvailable` column exists (safe for older DBs)."""
        try:
            cur = conn.execute("PRAGMA table_info(postList)")
            cols = [r[1] for r in cur.fetchall()]
            if 'isAvailable' not in cols:
                conn.execute("ALTER TABLE postList ADD COLUMN isAvailable INTEGER DEFAULT 1")
                conn.commit()
        except Exception:

            pass

    def createPost(self, conn: sqlite3.Connection):
        Post.create_table(conn)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO postList (userID, repliedPostID, title, content, media, timeCreated, viewCount, likeCount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, self.toTuple())
        conn.commit()
        self.postID = cur.lastrowid

    def deletePost(self, conn: sqlite3.Connection):
        if self.postID is None:
            return
        cur = conn.cursor()
        cur.execute("DELETE FROM postList WHERE postID = ?", (self.postID,))
        cur.execute("DELETE FROM postLikes WHERE postID = ?", (self.postID,))
        conn.commit()

    def mark_unavailable(self, conn: sqlite3.Connection):
        """Soft-remove the post by marking it as unavailable."""
        if self.postID is None:
            return
        try:
            Post.ensure_availability_column(conn)
            cur = conn.cursor()
            cur.execute("UPDATE postList SET isAvailable = 0 WHERE postID = ?", (self.postID,))
            conn.commit()
            self.isAvailable = 0
        except Exception:
            pass

    def incViewCount(self, conn: sqlite3.Connection):
        self.viewCount += 1
        if self.postID is not None:
            cur = conn.cursor()
            cur.execute("UPDATE postList SET viewCount = ? WHERE postID = ?", (self.viewCount, self.postID))
            conn.commit()

    def incLikeCount(self, conn: sqlite3.Connection):
        self.likeCount += 1
        if self.postID is not None:
            cur = conn.cursor()
            cur.execute("UPDATE postList SET likeCount = ? WHERE postID = ?", (self.likeCount, self.postID))
            conn.commit()

    @classmethod
    def has_user_liked(cls, conn: sqlite3.Connection, post_id: int, user_id: int) -> bool:
        if conn is None:
            return False
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM postLikes WHERE postID = ? AND userID = ? LIMIT 1", (post_id, user_id))
        return cur.fetchone() is not None

    @classmethod
    def toggle_like(cls, conn: sqlite3.Connection, post_id: int, user_id: int) -> int:
        if conn is None:
            return 0
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM postLikes WHERE postID = ? AND userID = ? LIMIT 1", (post_id, user_id))
        exists = cur.fetchone() is not None
        if exists:
            cur.execute("DELETE FROM postLikes WHERE postID = ? AND userID = ?", (post_id, user_id))
            cur.execute("UPDATE postList SET likeCount = MAX(0, likeCount - 1) WHERE postID = ?", (post_id,))
        else:
            try:
                cur.execute("INSERT INTO postLikes (postID, userID) VALUES (?, ?)", (post_id, user_id))
                cur.execute("UPDATE postList SET likeCount = likeCount + 1 WHERE postID = ?", (post_id,))
            except sqlite3.IntegrityError:
                pass
        conn.commit()
        cur.execute("SELECT likeCount FROM postList WHERE postID = ?", (post_id,))
        row = cur.fetchone()
        return int(row[0]) if row else 0

    def getTotalComments(self, conn: sqlite3.Connection) -> int:
        if self.postID is None:
            return 0
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM postList WHERE repliedPostID = ?", (self.postID,))
        return cur.fetchone()[0]

    def getAllComments(self, conn: sqlite3.Connection) -> List["Post"]:
        if self.postID is None:
            return []
        cur = conn.cursor()
        cur.execute("SELECT * FROM postList WHERE repliedPostID = ? ORDER BY timeCreated ASC", (self.postID,))
        rows = cur.fetchall()
        posts = []
        for r in rows :
            p = Post.fromRowSQL(r)
            if p is not None:
                posts.append(p)
        return posts

    def getUsernameByID(conn: sqlite3.Connection, user_id: int) -> str:
        if conn is None:
            return f"User {user_id}"
        
        try:
            cur = conn.execute("SELECT username FROM users WHERE userID = ?", (user_id,))
            row = cur.fetchone()
            if row:
                return row[0] if isinstance(row, tuple) else row['username']
            else:
                return f"User {user_id}"
        except Exception as e:
            print(f"⚠️ Error getting username for userID {user_id}: {e}")
            return f"User {user_id}"
        
    @classmethod
    def get_by_id(cls, conn: sqlite3.Connection, post_id: int) -> Optional["Post"]:
        cur = conn.execute("SELECT * FROM postList WHERE postID = ?", (post_id,))
        row = cur.fetchone()
        return cls.fromRowSQL(row) if row else None

    @classmethod
    def delete_by_id(cls, conn: sqlite3.Connection, post_id: int) -> None:
        cur = conn.cursor()
        cur.execute("DELETE FROM postList WHERE postID = ?", (post_id,))
        cur.execute("DELETE FROM postLikes WHERE postID = ?", (post_id,))
        conn.commit()

    @classmethod
    def set_unavailable_by_id(cls, conn: sqlite3.Connection, post_id: int) -> None:
        try:
            cls.ensure_availability_column(conn)
            cur = conn.cursor()
            cur.execute("UPDATE postList SET isAvailable = 0 WHERE postID = ?", (post_id,))
            conn.commit()
        except Exception:
            pass

    @classmethod
    def get_all_posts(cls, conn: sqlite3.Connection, order_by: str = "timeCreated", limit: Optional[int] = None) -> List["Post"]:
        mapping = {"timeCreated": "timeCreated", "likes": "likeCount", "views": "viewCount"}
        col = mapping.get(order_by, "timeCreated")
        q = f"SELECT * FROM postList ORDER BY {col} DESC"
        params: List[Any] = []
        if limit is not None:
            q += " LIMIT ?"
            params.append(int(limit))
        cur = conn.execute(q, tuple(params) if params else ())
        rows = cur.fetchall()
        return [cls.fromRowSQL(r) for r in rows if cls.fromRowSQL(r) is not None]



