import sqlite3
from datetime import datetime
import os
from models.UserModel import DB_FILE_PATH, GUIDE_FILE_PATH

class Plant:

    def __init__(self, userID, plantID, plantName, plantSpecies, 
                 plantingStartDate, plantMedia=None, waterFreqPerWeek=None, 
                 lightingDuration=None, waterVol=None, dailyLightingReq=None, 
                 fertilizerFreqPerWeek=None, fertilizerVol=None, plantPhase=None, height=0, 
                 problem=None, harvestEstim=None, leafColor=None):
        
        self.userID = userID
        self.plantID = plantID
        self.plantName = plantName
        self.plantSpecies = plantSpecies
        
        if isinstance(plantingStartDate, str):
            self.plantingStartDate = datetime.strptime(plantingStartDate, '%Y-%m-%d')
        else:
            self.plantingStartDate = plantingStartDate
            
        self.plantMedia = plantMedia
        self.waterFreqPerWeek = waterFreqPerWeek
        self.lightingDuration = lightingDuration
        self.waterVol = waterVol
        self.dailyLightingReq = dailyLightingReq
        self.fertilizerFreqPerWeek = fertilizerFreqPerWeek
        self.fertilizerVol = fertilizerVol
        self.plantPhase = plantPhase
        self.height = height
        self.problem = problem
        self.harvestEstim = harvestEstim
        self.leafColor = leafColor

    @staticmethod
    def _get_db_connection():
        conn = sqlite3.connect(DB_FILE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def initialize_table():
        conn = Plant._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants (
                plantID TEXT PRIMARY KEY,
                userID TEXT,
                plantName TEXT,
                plantSpecies TEXT,
                plantingStartDate TEXT,
                plantMedia TEXT,
                lightingDuration TEXT,
                height REAL,
                problem TEXT,
                leafColor TEXT,
            )
        ''')
        conn.commit()
        conn.close()

    def setRequirements(self):
        conn = sqlite3.connect(GUIDE_FILE_PATH)
        cursor = conn.cursor()
        age = int(self.calculateAgeInDays() / 7)
        cursor.execute('''SELECT
base_care_profiles.water_freq_days, base_care_profiles.water_vol_ml, 
base_care_profiles.sunlight_hours_req,
base_care_profiles.fert_freq_days, base_care_profiles.fert_vol_ml
FROM base_care_profiles INNER JOIN species
ON base_care_profiles.species_id = species.id
WHERE base_care_profiles.min_age_weeks <= ? AND base_care_profiles.max_age_weeks >= ?''',
(age, age,))
        result = cursor.fetchall()[0]
        self.setWateringFrequency(result[0])
        self.setWaterReq(result[1])
        self.setDailyLightingReq(result[2])
        self.setFertilizerFreq(result[3])
        self.setFertilizerReq(result[4])
        conn.close()


    def calculateAgeInDays(self):
        today = datetime.now()
        delta = today - self.plantingStartDate
        return delta.days

    # GETTER
    def getUserID(self):
        return self.userID

    def getPlantID(self):
        return self.plantID

    def getPlantName(self):
        return self.plantName

    def getPlantSpecies(self):
        return self.plantSpecies

    def getPlantingStartDate(self):
        return self.plantingStartDate

    def getPlantMedia(self):
        return self.plantMedia

    def getWateringFrequency(self):
        return self.waterFreqPerWeek

    def getLightingDuration(self):
        return self.lightingDuration

    def getWaterReq(self):
        return self.waterVol

    def getDailyLightingReq(self):
        return self.dailyLightingReq

    def getFertilizerReq(self):
        return self.fertilizerVol
    
    def getFertilizerFreq(self):
        return self.fertilizerFreqPerWeek

    def getPlantPhase(self):
        return self.plantPhase

    def getHeight(self):
        return self.height

    def getProblem(self):
        return self.problem

    def getHarvestEstim(self):
        return self.harvestEstim
    
    @staticmethod
    def getPlant(plantID_dicari, source_list):
        for tanaman in source_list:
            if tanaman.getPlantID() == plantID_dicari:
                return tanaman
        
        print("Tanaman tidak ditemukan!")
        return None

    # SETTER
    def setUserID(self, userID):
        self.userID = userID

    def setPlantID(self, plantID):
        self.plantID = plantID

    def setPlantName(self, plantName):
        self.plantName = plantName

    def setPlantSpecies(self, plantSpecies):
        self.plantSpecies = plantSpecies

    def setPlantingStartDate(self, plantingStartDate):
        if isinstance(plantingStartDate, str):
            self.plantingStartDate = datetime.strptime(plantingStartDate, '%Y-%m-%d')
        else:
            self.plantingStartDate = plantingStartDate

    def setPlantMedia(self, plantMedia):
        self.plantMedia = plantMedia

    def setWateringFrequency(self, wateringFrequency):
        self.waterFreqPerWeek = wateringFrequency

    def setLightingDuration(self, lightingDuration):
        self.lightingDuration = lightingDuration

    def setWaterReq(self, waterReq):
        self.waterVol = waterReq

    def setDailyLightingReq(self, dailyLightingReq):
        self.dailyLightingReq = dailyLightingReq

    def setFertilizerReq(self, fertilizerReq):
        self.fertilizerVol = fertilizerReq

    def setFertilizerFreq(self, fertilizerFreq):
        self.fertilizerFreqPerWeek = fertilizerFreq

    def setPlantPhase(self, plantPhase):
        self.plantPhase = plantPhase

    def setHeight(self, height):
        if height < 0:
            print("Error: Tinggi tanaman tidak boleh negatif.")
        else:
            self.height = height

    def setProblem(self, problem):
        self.problem = problem

    def setHarvestEstim(self, harvestEstim):
        self.harvestEstim = harvestEstim

    # OPERASI PADA DATABASE
    def addNewPlant(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            INSERT INTO plants (
                plantID, userID, plantName, plantSpecies, plantingStartDate,
                plantMedia, lightingDuration, height, problem, leafColor
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        date_str = self.plantingStartDate.strftime('%Y-%m-%d')
        
        values = (
            self.plantID, self.userID, self.plantName, self.plantSpecies, date_str,
            self.plantMedia, self.lightingDuration, self.height, self.problem, self.leafColor
        )
        
        try:
            cursor.execute(query, values)
            conn.commit()
            print(f"[DB Success] Tanaman '{self.plantName}' berhasil ditambahkan.")
            print(self.getDailyLightingReq(), end=": ")
            print(type(self.getDailyLightingReq()))
            print(self.getWateringFrequency(), end=": ")
            print(type(self.getWateringFrequency()))
            print(self.getWaterReq(), end=": ")
            print(type(self.getWaterReq()))
            print(self.getFertilizerFreq(), end=": ")
            print(type(self.getFertilizerFreq()))
            print(self.getFertilizerReq(), end=": ")
            print(type(self.getFertilizerReq()))
        except sqlite3.IntegrityError:
            print(f"[DB Error] ID Tanaman {self.plantID} sudah ada.")
        finally:
            conn.close()

    def removePlant(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM plants WHERE plantID = ?"
        cursor.execute(query, (self.plantID,))
        conn.commit()
        conn.close()
        print(f"[DB Success] Tanaman ID {self.plantID} berhasil dihapus.")

    def updatePlantData(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            UPDATE plants SET 
                plantName = ?, height = ?, plantPhase = ?, problem = ?
            WHERE plantID = ?
        '''
        
        values = (self.plantName, self.height, self.plantPhase, self.problem, self.plantID)
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        print(f"[DB Success] Data tanaman {self.plantID} berhasil diupdate.")

    @classmethod
    def getAllPlant(cls, userID):
        conn = cls._get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM plants WHERE userID = ?"
        cursor.execute(query, (userID,))
        rows = cursor.fetchall()
        conn.close()

        plant_list = []
        for row in rows:
            plant_obj = cls(
                userID=row['userID'],
                plantID=row['plantID'],
                plantName=row['plantName'],
                plantSpecies=row['plantSpecies'],
                plantingStartDate=row['plantingStartDate'],
                plantMedia=row['plantMedia'],
                lightingDuration=row['lightingDuration'],
                height=row['height'],
                problem=row['problem'],
                leafColor=row['leafColor']
            )
            plant_list.append(plant_obj)
        
        return plant_list