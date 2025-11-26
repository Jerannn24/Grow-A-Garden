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

            plant_phase, harvest_date_str = Plant.calculate_dynamic_attributes(
                dataForm['species'], 
                planting_start_date
            )
            
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
            
            print("Manager: Mencoba menyimpan ke Database...")
            try:
                new_plant.addNewPlant()
                print("Manager: Berhasil simpan ke DB.")
                
            except Exception as db_error:
                print(f"Manager DB ERROR: {db_error}")
                raise db_error 

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
        plant_to_delete = None
        for plant in self.plantList:
            if plant.plantID == plantID:
                plant_to_delete = plant
                break
        
        if plant_to_delete:
            try:
                plant_to_delete.removePlant() 

                self.plantList.remove(plant_to_delete)
                
                print(f"✅ PlantManager: Tanaman {plantID} berhasil dihapus dari list & DB.")
                return True
            except Exception as e:
                print(f"❌ PlantManager Error: Gagal menghapus tanaman. {e}")
                return False
        else:
            print("⚠️ PlantManager: Tanaman tidak ditemukan di list.")
            return False