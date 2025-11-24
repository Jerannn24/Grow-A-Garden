import sys
import os
import traceback 

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

from src.models.Plant import Plant

class PlantManager:
    
    def __init__(self):
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

    def onAddClick(self, dataForm):
        print("Manager: Memproses dataForm...", dataForm)
        
        try:
            new_plant = Plant(
                userID=dataForm['userID'],
                plantID=dataForm['plantID'],
                plantName=dataForm['name'],
                plantSpecies=dataForm['species'],
                plantingStartDate=dataForm['date'],
                plantMedia=dataForm['media'],
                lightingDuration=dataForm['sunlight_habit']
            )
            
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