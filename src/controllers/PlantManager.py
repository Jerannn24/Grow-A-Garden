import sys
import os
import traceback # Untuk melihat detail error
import sqlite3
from datetime import datetime, timedelta
from models.UserModel import DB_FILE_PATH, GUIDE_FILE_PATH

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

from models.Plant import Plant

class PlantManager:
    
    def __init__(self):
        self.user_db_path = DB_FILE_PATH
        self.guide_db_path = GUIDE_FILE_PATH
        self.plantList = []
        print("Manager: Memeriksa tabel database...")
        try:
            Plant.initialize_table()
            print("Manager: Tabel database siap.")
        except Exception as e:
            print(f"Manager CRITICAL ERROR: Gagal membuat tabel! {e}")
    
    def loadUserData(self, userID):
        print("Manager: Meminta Model mengambil semua data dari DB...")
        try:
            self.plantList = Plant.getAllPlant(userID)
            print(f"Manager: List Lokal terisi {len(self.plantList)} tanaman.")
        except Exception as e:
            print(f"Manager Error (Load): {e}")
            self.plantList = []

        
    def getPlant(self, plantID):
        return Plant.getPlant(plantID, self.plantList)

    def onAddClick(self, dataForm: dict[str, any]):
        print("Manager: Memproses dataForm...", dataForm)
        
        try:
            acquired_date = datetime.strptime(dataForm["date_acquired"], "%Y-%m-%d")
            days_old_at_acquisition = dataForm["initial_age_months"] * 30
            planting_start_date = acquired_date - timedelta(days=days_old_at_acquisition)

            age_days_total = (datetime.now() - planting_start_date).days
            current_age_weeks = max(0, age_days_total / 7)
            plant_phase, harvest_date_str = self._calculate_smart_attributes(
                dataForm['species'], 
                current_age_weeks, 
                planting_start_date
            )
            # TODO: ambil data dari plants.db
            
            new_plant = Plant(
                userID=dataForm['userID'],
                plantID=dataForm['plantID'],
                plantName=dataForm['name'],
                plantSpecies=dataForm['species'],
                plantingStartDate=planting_start_date.strftime('%Y-%m-%d'),
                plantMedia=dataForm['media'],
                lightingDuration=dataForm['sunlight_habit'],
                height=dataForm.get('current_height_cm', 0),
                leafColor=dataForm['current_leaf_color'],
                plantPhase=plant_phase,
                harvestEstim=harvest_date_str,
            )
            new_plant.setRequirements()
            
            # 2. Simpan ke Database (Coba blok ini dengan hati-hati)
            print("Manager: Mencoba menyimpan ke Database...")
            try:
                new_plant.addNewPlant()
                print("Manager: Berhasil simpan ke DB.")
                
            except Exception as db_error:
                print(f"Manager DB ERROR: {db_error}")
                raise db_error 

            self.plantList.append(new_plant)
            print("--- DEBUG ON ADD ---")
            print(f"ID Objek PlantManager (saat add): {id(self)}")
            print(f"Isi plantList sekarang: {self.plantList}")
            print(f"Manager: List Lokal diupdate. Total: {len(self.plantList)}")
            
        except Exception as e:
            print("------------------------------------------------")
            print(f"Manager GAGAL Menambah Tanaman: {e}")
            print("Detail Error:")
            traceback.print_exc() 
            print("------------------------------------------------")


    def _calculate_smart_attributes(self, species_name, current_age_weeks, planting_start_date):
        """
        Helper: Melakukan 3-Step DB Lookup untuk Phase & Harvest
        """
        default_phase = "Vegetative" # Default jika data tidak ditemukan
        default_harvest = "Unknown"
        
        conn = sqlite3.connect(self.guide_db_path)
        cursor = conn.cursor()
        
        try:
            # LANGKAH 1: Dapatkan SPECIES_ID
            # Kita cari ID berdasarkan nama spesies (Case insensitive dengan LIKE)
            cursor.execute("SELECT id FROM species WHERE common_name LIKE ?", (species_name,))
            row = cursor.fetchone()
            
            if not row:
                print(f"[SmartLogic] Spesies '{species_name}' tidak ditemukan di DB referensi.")
                return default_phase, default_harvest
            
            species_id = row[0]

            # LANGKAH 2: Tentukan PLANT PHASE
            # Cari fase di mana umur sekarang berada di antara MIN dan MAX
            cursor.execute("""
                SELECT stage_name 
                FROM base_care_profiles 
                WHERE species_id = ? 
                  AND ? >= min_age_weeks 
                  AND ? <= max_age_weeks
            """, (species_id, current_age_weeks, current_age_weeks))
            
            phase_row = cursor.fetchone()
            final_phase = phase_row[0] if phase_row else default_phase

            # LANGKAH 3: Tentukan HARVEST ESTIMATION
            cursor.execute("""
                SELECT min_time_to_harvest_days, max_time_to_harvest_days 
                FROM harvest_info 
                WHERE species_id = ?
            """, (species_id,))
            
            harvest_row = cursor.fetchone()
            final_harvest_str = default_harvest
            
            if harvest_row:
                min_days = harvest_row[0]
                max_days = harvest_row[1]
                
                # 1. Hitung total hari yang dibutuhkan dari awal tanam sampai panen
                avg_days_needed = (min_days + max_days) / 2
                
                # 2. Tentukan Tanggal Target Panen (Kapan seharusnya panen?)
                target_harvest_date = planting_start_date + timedelta(days=avg_days_needed)
                
                # 3. Bandingkan dengan HARI INI (Countdown)
                today = datetime.now()
                delta = target_harvest_date - today
                
                days_left = delta.days + 1 # +1 agar pembulatan hari lebih masuk akal
                
                # 4. Format String Output
                if days_left > 1:
                    final_harvest_str = f"{days_left} days left"
                elif days_left == 1:
                    final_harvest_str = "Tomorrow!"
                elif days_left == 0:
                    final_harvest_str = "Harvest Today! 🌾"
                else:
                    # Jika lewat tanggal panen (Overdue)
                    final_harvest_str = f"Ready! ({abs(days_left)}d ago)"

            return final_phase, final_harvest_str

        except Exception as e:
            print(f"[SmartLogic Error] {e}")
            return default_phase, default_harvest
        finally:
            conn.close()

    def onDeleteClick(self, plantID):
        """
        Menghapus tanaman dari Database (via Model) dan List Memory.
        Dipanggil oleh HomePage setelah konfirmasi user.
        """
        # 1. Cari objek tanaman di dalam list memory
        plant_to_delete = None
        for plant in self.plantList:
            if plant.plantID == plantID:
                plant_to_delete = plant
                break
        
        if plant_to_delete:
            try:
                # 2. Panggil metode removePlant() milik MODEL (Plant.py)
                # Ini akan menjalankan query DELETE di database sesuai kode yang kamu punya
                plant_to_delete.removePlant() 

                # 3. Hapus dari Memory List Manager agar sinkron
                self.plantList.remove(plant_to_delete)
                
                print(f"✅ PlantManager: Tanaman {plantID} berhasil dihapus dari list & DB.")
                return True
            except Exception as e:
                print(f"❌ PlantManager Error: Gagal menghapus tanaman. {e}")
                return False
        else:
            print("⚠️ PlantManager: Tanaman tidak ditemukan di list.")
            return False