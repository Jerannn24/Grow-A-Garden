import sqlite3
from datetime import datetime
from models.UserModel import DB_FILE_PATH

class Plant:
    def __init__(self, userID, plantID, plantName, plantSpecies, 
                 plantingStartDate, plantMedia, wateringFrequency, 
                 lightingDuration, dailyWaterReq=None, dailyLightingReq=None, 
                 fertilizerReq=None, plantPhase="Germination", height=0, 
                 problem=None, harvestEstim=None):
        
        self.userID = userID
        self.plantID = plantID
        self.plantName = plantName
        self.plantSpecies = plantSpecies
        
        if isinstance(plantingStartDate, str):
            self.plantingStartDate = datetime.strptime(plantingStartDate, '%Y-%m-%d')
        else:
            self.plantingStartDate = plantingStartDate
            
        self.plantMedia = plantMedia
        self.wateringFrequency = wateringFrequency
        self.lightingDuration = lightingDuration
        self.dailyWaterReq = dailyWaterReq
        self.dailyLightingReq = dailyLightingReq
        self.fertilizerReq = fertilizerReq
        self.plantPhase = plantPhase
        self.height = height
        self.problem = problem
        self.harvestEstim = harvestEstim

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
                wateringFrequency TEXT,
                lightingDuration TEXT,
                dailyWaterReq TEXT,
                dailyLightingReq TEXT,
                fertilizerReq TEXT,
                plantPhase TEXT,
                height REAL,
                problem TEXT,
                harvestEstim TEXT
            )
        ''')
        conn.commit()
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
        return self.wateringFrequency

    def getLightingDuration(self):
        return self.lightingDuration

    def getDailyWaterReq(self):
        return self.dailyWaterReq

    def getDailyLightingReq(self):
        return self.dailyLightingReq

    def getFertilizerReq(self):
        return self.fertilizerReq

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
        self.wateringFrequency = wateringFrequency

    def setLightingDuration(self, lightingDuration):
        self.lightingDuration = lightingDuration

    def setDailyWaterReq(self, dailyWaterReq):
        self.dailyWaterReq = dailyWaterReq

    def setDailyLightingReq(self, dailyLightingReq):
        self.dailyLightingReq = dailyLightingReq

    def setFertilizerReq(self, fertilizerReq):
        self.fertilizerReq = fertilizerReq

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
                plantMedia, wateringFrequency, lightingDuration, dailyWaterReq,
                dailyLightingReq, fertilizerReq, plantPhase, height, problem, harvestEstim
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        date_str = self.plantingStartDate.strftime('%Y-%m-%d')
        
        values = (
            self.plantID, self.userID, self.plantName, self.plantSpecies, date_str,
            self.plantMedia, self.wateringFrequency, self.lightingDuration, self.dailyWaterReq,
            self.dailyLightingReq, self.fertilizerReq, self.plantPhase, self.height, 
            self.problem, self.harvestEstim
        )
        
        try:
            cursor.execute(query, values)
            conn.commit()
            print(f"[DB Success] Tanaman '{self.plantName}' berhasil ditambahkan.")
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
                wateringFrequency=row['wateringFrequency'],
                lightingDuration=row['lightingDuration'],
                dailyWaterReq=row['dailyWaterReq'],
                dailyLightingReq=row['dailyLightingReq'],
                fertilizerReq=row['fertilizerReq'],
                plantPhase=row['plantPhase'],
                height=row['height'],
                problem=row['problem'],
                harvestEstim=row['harvestEstim']
            )
            plant_list.append(plant_obj)
        
        return plant_list