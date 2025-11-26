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
            # 1. Hitung Tanggal & Umur
            acquired_date = datetime.strptime(dataForm["date_acquired"], "%Y-%m-%d")
            days_old_at_acquisition = dataForm["initial_age_months"] * 30
            planting_start_date = acquired_date - timedelta(days=days_old_at_acquisition)

            # Tidak perlu hitung manual age_days_total di sini lagi karena helper di Plant sudah menghitungnya
            
            # 2. [PERBAIKAN DI SINI] 
            # Panggil fungsi Static dari Class Plant, BUKAN self
            plant_phase, harvest_date_str = Plant.calculate_dynamic_attributes(
                dataForm['species'], 
                planting_start_date
            )
            
            # 3. Buat Objek Plant
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
                
                # Masukkan hasil hitungan tadi
                plantPhase=plant_phase,
                harvestEstim=harvest_date_str,
            )
            
            # 4. Ambil kebutuhan air/pupuk (Opsional)
            new_plant.setRequirements()
            
            # 5. Simpan ke Database
            print("Manager: Mencoba menyimpan ke Database...")
            new_plant.addNewPlant() 
            print("Manager: Berhasil simpan ke DB.")

            # 6. Update List Lokal
            self.plantList.append(new_plant)
            
            return True
            
        except Exception as e:
            print(f"Manager GAGAL Menambah Tanaman: {e}")
            try:
                import traceback
                traceback.print_exc()
            except:
                pass
            return False
        
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