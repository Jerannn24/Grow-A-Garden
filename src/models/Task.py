from datetime import datetime, timedelta
import sqlite3
from models.Plant import Plant
from models.UserModel import DB_FILE_PATH, GUIDE_FILE_PATH
from collections import defaultdict

class Task:
    def __init__(self, taskID, plantID, actionType: str, quantity=0, status=False, deadline=None):
        self.taskID = taskID
        self.plantID = plantID
        self.actionType = actionType
        self.quantity = quantity
        self.status = status
        self.deadline = deadline or datetime.now()

    def is_overdue(self):
        return not self.status and self.deadline < datetime.now()

    def __repr__(self):
        return f"Task({self.taskID}, {self.plantID}, {self.actionType}, deadline={self.deadline})"
    
    @staticmethod
    def getConnectionApp():
        conn = sqlite3.connect(DB_FILE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def getConnectionGuide():
        conn = sqlite3.connect(GUIDE_FILE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    # membuat tabel di app.db
    @staticmethod
    def init_table():
        """Membuat tabel tasks di app.db"""
        conn = Task.getConnectionApp()
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
                     task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     plant_id TEXT,
                     action_type TEXT,
                     quantity INTEGER,
                     status INTEGER,
                     deadline TEXT,
                     actual_quantity INTEGER,
                     time_done TEXT );
""")
        conn.commit()
        conn.close()

    # return dictionary {plant_id: [...Task]} untuk hari ini
    @staticmethod
    def getTodaysTodo(user_id, plant_id=None):
        """Mengembalikan task yang deadline-nya hari ini

        Parameters:
            user_id (int): ID current user
            plant_id (str | None): ID tanaman yang akan diambil task-nya (optional)

        Returns:
            grouped: dict plant_id ke List of Task
        """
        conn = Task.getConnectionApp()
        cursor = conn.cursor()

        if plant_id:
            query = """
            SELECT * FROM tasks
            WHERE user_id = ?
            AND plant_id = ?
            AND date(deadline) = date('now', '+7 hours');
            """
            cursor.execute(query, (user_id, plant_id))
            print(f"[DEBUG] getTodaysTodo query: user_id={user_id}, plant_id={plant_id}")
        else:
            query = """
            SELECT * FROM tasks
            WHERE user_id = ?
            AND date(deadline) = date('now', '+7 hours');
            """
            cursor.execute(query, (user_id,))
            print(f"[DEBUG] getTodaysTodo query: user_id={user_id}")

        rows = cursor.fetchall()
        print(f"[DEBUG] getTodaysTodo rows count: {len(rows)}")
        
        # Debug: Also check ALL tasks for this user
        if len(rows) == 0:
            cursor.execute("SELECT * FROM tasks WHERE user_id = ? LIMIT 5", (user_id,))
            all_tasks = cursor.fetchall()
            print(f"[DEBUG] All tasks for user_id={user_id}: {len(all_tasks)} total")
            for t in all_tasks:
                print(f"  - Task: id={t['task_id']}, plant={t['plant_id']}, deadline={t['deadline']}, action={t['action_type']}")
        
        grouped = defaultdict(list)

        for row in rows:
            try:
                deadline_dt = datetime.strptime(row['deadline'], "%Y-%m-%d %H:%M:%S")
            except:
                deadline_dt = datetime.strptime(row['deadline'], "%Y-%m-%d")

            task_obj = Task(row['task_id'], row['plant_id'], row['action_type'],
                            row['quantity'], bool(row['status']), deadline_dt)

            grouped[row['plant_id']].append(task_obj)
                    
        conn.close()

        return dict(grouped)
    
    # return dictionary {plant_id: [...Task]} untuk 7 hari ke depan minus hari ini
    @staticmethod
    def getWeeksTodo(user_id, plant_id=None):
        conn = Task.getConnectionApp()
        cursor = conn.cursor()

        if plant_id:
            query = """
            SELECT * FROM tasks
            WHERE user_id = ?
            AND plant_id = ?
            AND date(deadline) > date('now', '+7 hours')
            AND date(deadline) <= date('now', '+7 hours', '+7 days')
            ORDER BY plant_id, deadline;
            """
            cursor.execute(query, (user_id, plant_id))
        else:
            query = """
            SELECT * FROM tasks
            WHERE user_id = ?
            AND date(deadline) > date('now', '+7 hours')
            AND date(deadline) <= date('now', '+7 hours', '+7 days')
            ORDER BY plant_id, deadline;
            """
            cursor.execute(query, (user_id,))

        rows = cursor.fetchall()

        grouped = defaultdict(list)

        for row in rows:
            try:
                deadline_dt = datetime.strptime(row['deadline'], "%Y-%m-%d %H:%M:%S")
            except:
                deadline_dt = datetime.strptime(row['deadline'], "%Y-%m-%d")

            task = Task(
                taskID=row['task_id'],
                plantID=row['plant_id'],
                actionType=row['action_type'],
                quantity=row['quantity'],
                status=bool(row['status']),
                deadline=deadline_dt
            )

            grouped[row['plant_id']].append(task)
        
        print(f"[DEBUG] getWeeksTodo rows count: {len(rows)}, grouped keys: {list(grouped.keys())}")
                    
        conn.close()

        return dict(grouped)
    
    # return dictionary {plant_id: [...Task]} yang deadline < hari ini
    @staticmethod
    def getOverdueTasks(user_id, plant_id=None):
        conn = Task.getConnectionApp()
        cursor = conn.cursor()

        if plant_id:
            query = """
            SELECT * FROM tasks
            WHERE user_id = ?
            AND plant_id = ?
            AND status = 0
            AND date(deadline) < date('now', '+7 hours')
            ORDER BY plant_id, deadline;
            """
            cursor.execute(query, (user_id, plant_id))
        else:
            query = """
            SELECT * FROM tasks
            WHERE user_id = ?
            AND status = 0
            AND date(deadline) < date('now', '+7 hours')
            ORDER BY plant_id, deadline;
            """
            cursor.execute(query, (user_id,))

        rows = cursor.fetchall()

        grouped = defaultdict(list)

        for row in rows:
            try:
                deadline_dt = datetime.strptime(row['deadline'], "%Y-%m-%d %H:%M:%S")
            except:
                deadline_dt = datetime.strptime(row['deadline'], "%Y-%m-%d")

            task = Task(
                taskID=row['task_id'],
                plantID=row['plant_id'],
                actionType=row['action_type'],
                quantity=row['quantity'],
                status=bool(row['status']),
                deadline=deadline_dt
            )

            grouped[row['plant_id']].append(task)
        
        print(f"[DEBUG] getOverdueTasks rows count: {len(rows)}, grouped keys: {list(grouped.keys())}")

        conn.close()

        return dict(grouped)
    
    @staticmethod
    def getCompletedTasks(user_id, plant_id=None):
        """Get all completed tasks for a user, optionally filtered by plant_id"""
        conn = Task.getConnectionApp()
        cursor = conn.cursor()
        
        if plant_id:
            cursor.execute("""
                SELECT * FROM tasks
                WHERE user_id = ? AND plant_id = ? AND status = 1
                ORDER BY datetime(time_done) DESC
                LIMIT 50
            """, (user_id, plant_id))
        else:
            cursor.execute("""
                SELECT * FROM tasks
                WHERE user_id = ? AND status = 1
                ORDER BY datetime(time_done) DESC
                LIMIT 50
            """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        tasks_by_plant = {}
        for row in rows:
            try:
                deadline_dt = datetime.strptime(row['deadline'], "%Y-%m-%d %H:%M:%S")
            except:
                deadline_dt = datetime.strptime(row['deadline'], "%Y-%m-%d")
            
            task = Task(
                taskID=row['task_id'],
                plantID=row['plant_id'],
                actionType=row['action_type'],
                quantity=row['quantity'],
                status=bool(row['status']),
                deadline=deadline_dt
            )
            
            plant_id_key = row['plant_id']
            if plant_id_key not in tasks_by_plant:
                tasks_by_plant[plant_id_key] = []
            tasks_by_plant[plant_id_key].append(task)
        
        print(f"[DEBUG] getCompletedTasks rows count: {len(rows)}, grouped keys: {list(tasks_by_plant.keys())}")
        return tasks_by_plant
    
    # return rasio actual_quantity / quantity 
    @staticmethod
    def getCarePercentage(plant_id, action_type):
        conn = Task.getConnectionApp()
        cursor = conn.cursor()
        query = """
    SELECT quantity, actual_quantity FROM tasks
    WHERE plant_id = ?
    AND action_type = ?
    AND date(deadline) > date('now', '+7 hours', '-7 days')
    AND date(deadline) <= date('now', '+7 hours');
"""
        cursor.execute(query, ( plant_id, action_type,))
        if cursor.rowcount == 0:
            return 1.0
        history = cursor.fetchall()
        sum_required = 0
        sum_actual = 0
        for action in history:
            sum_required += action['quantity']
            sum_actual += action['actual_quantity']
        
        if sum_required == 0:
            return 1.0
        return float(sum_actual) / sum_required
    
    @staticmethod
    def refreshLog(user_id):
        appConn = Task.getConnectionApp()
        appCursor = appConn.cursor()
        garden = Plant.getAllPlant(userID=user_id)
        for plant in garden:
            plant.setRequirements()
            water_hour_gap = 7 * 24 // plant.waterFreqPerWeek
            water_threshold = datetime().now() - timedelta(hours=water_hour_gap)
            query = """
            UPDATE tasks
            SET status = 1,
            actual_quantity = 0,
            time_done = datetime('now')
            WHERE status = 0
            AND datetime(deadline) < datetime(?)
            AND action_type = 'water'
            AND plant_id = ?;
            """
            appCursor.execute(query, (water_threshold, plant.plantID,))
        appConn.commit()
        appConn.close()
    
    @staticmethod
    def regenerateTask(user_id, action_type=None, plant_id=None):
        conn = Task.getConnectionApp()
        cursor = conn.cursor()
        print(f"[DEBUG-REGEN] regenerateTask called: user_id={user_id}, plant_id={plant_id}, action_type={action_type}")

        # Ambil tanaman relevan
        if plant_id:
            cursor.execute("""
                SELECT * FROM plants
                WHERE plantID = ? AND userID = ?
            """, (plant_id, user_id))
        else:
            cursor.execute("""
                SELECT * FROM plants
                WHERE userID = ?
            """, (user_id,))
        plants = cursor.fetchall()
        print(f"[DEBUG-REGEN] Plants found: {len(plants)}")

        now = datetime.now()
        seven_days_after = now + timedelta(days=7)

        for plant in plants:
            pid = plant["plantID"]
            print(f"[DEBUG-REGEN] Processing plant_id={pid}")
            
            # Create a Plant object with all required fields from the database
            try:
                # Convert sqlite3.Row to dict
                plant_dict = dict(plant)
                obj = Plant(
                    userID=plant_dict.get("userID"),
                    plantID=plant_dict.get("plantID"),
                    plantName=plant_dict.get("plantName"),
                    plantSpecies=plant_dict.get("plantSpecies"),
                    plantingStartDate=plant_dict.get("plantingStartDate"),
                    plantMedia=plant_dict.get("plantMedia"),
                    waterFreqPerWeek=plant_dict.get("waterFreqPerWeek"),
                    lightingDuration=plant_dict.get("lightingDuration"),
                    waterVol=plant_dict.get("waterVol"),
                    dailyLightingReq=plant_dict.get("dailyLightingReq"),
                    fertilizerFreqPerWeek=plant_dict.get("fertilizerFreqPerWeek"),
                    fertilizerVol=plant_dict.get("fertilizerVol"),
                    plantPhase=plant_dict.get("plantPhase"),
                    height=plant_dict.get("height"),
                    harvestEstim=plant_dict.get("harvestEstim"),
                    leafColor=plant_dict.get("leafColor")
                )
                obj.setRequirements()  # agar waterFreqPerWeek dsb terisi
                print(f"[DEBUG-REGEN]   waterFreqPerWeek={obj.waterFreqPerWeek}, fertilizerFreqPerWeek={obj.fertilizerFreqPerWeek}, dailyLightingReq={obj.dailyLightingReq}")
            except Exception as e:
                print(f"[DEBUG-REGEN] ERROR creating Plant object: {e}")
                import traceback
                traceback.print_exc()
                continue

            # Tentukan action mana yang akan dibuat ulang
            actions = []
            if action_type:
                actions = [action_type]
            else:
                actions = ["water", "fertilize", "harvest", "light", "update"]

            for action in actions:

                # Tentukan interval berdasarkan action
                if action == "water":
                    if obj.waterFreqPerWeek <= 0:
                        print(f"[DEBUG-REGEN]   Action 'water' skipped (frequency={obj.waterFreqPerWeek})")
                        continue
                    interval = timedelta(hours=(7*24 / obj.waterFreqPerWeek))

                elif action == "fertilize":
                    if obj.fertilizerFreqPerWeek <= 0:
                        print(f"[DEBUG-REGEN]   Action 'fertilize' skipped (frequency={obj.fertilizerFreqPerWeek})")
                        continue
                    interval = timedelta(hours=(7*24 / obj.fertilizerFreqPerWeek))

                elif action == "light":
                    if obj.dailyLightingReq <= 0:
                        print(f"[DEBUG-REGEN]   Action 'light' skipped (requirement={obj.dailyLightingReq})")
                        continue
                    # Light tasks should ALWAYS be every 24 hours, not based on dailyLightingReq
                    interval = timedelta(hours=24)
                    print(f"[DEBUG-REGEN]   Light interval set to 24 hours (dailyLightingReq={obj.dailyLightingReq})")

                elif action == "harvest":
                    # For harvest, calculate based on harvest estimate date
                    try:
                        harvest_date = obj.calculate_harvest_estim()
                        if harvest_date and harvest_date > datetime.now():
                            # Calculate days until harvest
                            days_to_harvest = (harvest_date - datetime.now()).days
                            interval = timedelta(days=max(1, days_to_harvest))
                        else:
                            # Already passed or invalid, skip
                            print(f"[DEBUG-REGEN]   Action 'harvest' skipped (date already passed or invalid)")
                            continue
                    except Exception as e:
                        print(f"[DEBUG-REGEN]   Action 'harvest' error: {e}")
                        continue

                else:
                    if action == "update":
                        interval = timedelta(days=7)
                    else:
                        continue
                
                print(f"[DEBUG-REGEN]   Action '{action}' interval: {interval}")

                # Ambil task terakhir yang selesai
                cursor.execute("""
                    SELECT deadline FROM tasks
                    WHERE user_id = ? AND plant_id = ? AND action_type = ?
                    AND status = 1
                    ORDER BY datetime(deadline) DESC
                    LIMIT 1
                """, (user_id, pid, action))
                last_done = cursor.fetchone()

                if last_done:
                    try:
                        last_time = datetime.strptime(last_done["deadline"], "%Y-%m-%d %H:%M:%S")
                    except:
                        last_time = datetime.strptime(last_done["deadline"], "%Y-%m-%d")
                else:
                    # Belum pernah mengerjakan, mulai hari ini
                    last_time = now

                # Hapus task mendatang yang salah (agar tidak numpuk)
                cursor.execute("""
                    DELETE FROM tasks
                    WHERE user_id = ? AND plant_id = ? AND action_type = ?
                    AND date(deadline) > date('now', '+7 hours')
                    AND date(deadline) <= date('now', '+7 hours', '+7 days')
                """, (user_id, pid, action))
                
                # For light tasks, also delete future incomplete tasks to ensure 24-hour interval
                if action == "light":
                    cursor.execute("""
                        DELETE FROM tasks
                        WHERE user_id = ? AND plant_id = ? AND action_type = ?
                        AND status = 0
                        AND datetime(deadline) > datetime('now')
                    """, (user_id, pid, action))
                    print(f"[DEBUG-REGEN]   Cleaned up old light tasks for plant_id={pid}")

                # Generate ulang task sampai 7 hari ke depan
                next_time = last_time + interval

                if action == "harvest":
                    print(f"[DEBUG-REGEN]     INSERT harvest task for deadline={next_time}")
                    cursor.execute("""
                        INSERT INTO tasks (user_id, plant_id, action_type, quantity, status, deadline)
                        VALUES (?, ?, ?, ?, 0, ?)
                    """, (user_id, pid, action, 0, next_time.strftime("%Y-%m-%d %H:%M:%S")))
                elif action == "update":
                    tasks_added = 0
                    while next_time <= seven_days_after:
                        cursor.execute("""
                            INSERT INTO tasks (user_id, plant_id, action_type, quantity, status, deadline)
                            VALUES (?, ?, ?, ?, 0, ?)
                        """, (user_id, pid, action, 0, next_time.strftime("%Y-%m-%d %H:%M:%S")))
                        tasks_added += 1
                        next_time += interval
                    print(f"[DEBUG-REGEN]     INSERT {tasks_added} 'update' tasks")
                else:
                    task_count = 0
                    while next_time <= seven_days_after:
                        cursor.execute("""
                            INSERT INTO tasks (user_id, plant_id, action_type, quantity, status, deadline)
                            VALUES (?, ?, ?, ?, 0, ?)
                        """, (user_id, pid, action, 0, next_time.strftime("%Y-%m-%d %H:%M:%S")))
                        task_count += 1
                        next_time += interval
                    print(f"[DEBUG-REGEN]     INSERT {task_count} '{action}' tasks")

        conn.commit()
        print(f"[DEBUG-REGEN] Tasks committed to database")
        conn.close()

    @staticmethod
    def completeTask(task_id, actual_quantity):
        """Mark a task as completed and record actual quantity"""
        conn = Task.getConnectionApp()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks
            SET status = 1,
                actual_quantity = ?,
                time_done = datetime('now')
            WHERE task_id = ?
        """, (actual_quantity, task_id))
        
        conn.commit()
        conn.close()
        print(f"[DEBUG] Task {task_id} marked as complete with quantity {actual_quantity}")

    @staticmethod
    def scheduleGrowthUpdate(user_id, plant_id, start_from=None):
        """Create the next 'update' task exactly 7 days after the provided base time."""
        base_time = start_from or datetime.now()
        due_time = base_time + timedelta(days=7)

        conn = Task.getConnectionApp()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT COUNT(*) FROM tasks
                WHERE user_id = ? AND plant_id = ? AND action_type = 'update'
                AND status = 0 AND datetime(deadline) BETWEEN datetime('now') AND datetime('now', '+7 days')
                """,
                (user_id, plant_id)
            )
            already_exists = cursor.fetchone()[0]
            if already_exists:
                return False

            cursor.execute(
                """
                INSERT INTO tasks (user_id, plant_id, action_type, quantity, status, deadline)
                VALUES (?, ?, 'update', 0, 0, ?)
                """,
                (user_id, plant_id, due_time.strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            return True
        except Exception as exc:
            print(f"[DEBUG] scheduleGrowthUpdate failed: {exc}")
            conn.rollback()
            return False
        finally:
            conn.close()
