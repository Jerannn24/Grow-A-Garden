from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QGridLayout, QMessageBox, QDialog
from PyQt5.QtCore import Qt

from controllers.PlantManager import PlantManager
from views.AddPlantForm import AddPlantForm
from .PlantCard import PlantCard
from .AddPlantCard import AddPlantCard
from .AppHeader import AppHeader


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.plant_manager = PlantManager()
        self.current_user_id = None
        # Load data awal dari DB ke memory
        self.plant_manager.loadUserData(self.current_user_id) 

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(10)
        
        self.main_layout.addWidget(AppHeader("My Garden", "Monitor and manage your plants' health"))
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        self.content_widget = QWidget()
        self.grid = QGridLayout(self.content_widget)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        max_cols = 3 
        for i in range(max_cols): 
            self.grid.setColumnStretch(i, 1)
        
        self.scroll.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll)

        self.refresh_plant_list()

    def refresh_plant_list(self):
        """Menghapus kartu lama dan menggambar ulang berdasarkan data terbaru."""
        print("--- DEBUG REFRESH ---")
        print(f"ID Objek PlantManager: {id(self.plant_manager)}")
        print(f"Isi plantList: {self.plant_manager.plantList}")
        
        if not self.current_user_id:
            print("Peringatan: UserID belum diset. Tidak memuat tanaman.")
            return
        
        for i in reversed(range(self.grid.count())): 
            widget = self.grid.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None) 
                widget.deleteLater()   

        add_card = AddPlantCard()
        add_card.clicked.connect(self.open_add_plant_form)
        self.grid.addWidget(add_card, 0, 0)

        # Ambil Data dari manager
        plants = self.plant_manager.plantList 

        print(f"Debug: Menampilkan {len(plants)} tanaman.") 

        # Loop buat nampilin tanaman
        row = 0
        col = 1 # Col 1 karena col 0 buat add plant
        max_cols = 3 

        for plant in plants:
            p_name = plant.getPlantName()
            p_species = plant.getPlantSpecies()
            p_media = plant.getPlantMedia()
            p_sun = "Sun" 

            stats = {"🌱": p_media, "☀️": p_sun}
            
            card = PlantCard(
                name=p_name,
                sci_name=p_species,
                stats=stats,
                action_text="Details" 
            )
            
            self.grid.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0      
                row += 1     
            
            if row == 0 and col == 0:
                col = 1
                
    def set_current_user_id(self, userID: int):
        if self.current_user_id != userID:
            self.current_user_id = userID
            # Muat data saat UserID sudah valid
            self.plant_manager.loadUserData(self.current_user_id)
            self.refresh_plant_list()
    
    def open_add_plant_form(self):
        """Membuka dialog tambah tanaman."""
        if not self.current_user_id:
             QMessageBox.critical(self, "Error", "UserID belum terdeteksi. Silakan login ulang.")
             return
         
        form = AddPlantForm(self)
        
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            
            data['userID'] = self.current_user_id
            import time
            data['plantID'] = f"P{int(time.time())}" 
            data['date'] = "2025-01-01" 
            
            print("Debug: Mengirim data ke Manager:", data)

            self.plant_manager.onAddClick(data) 
            self.refresh_plant_list()
            
            QMessageBox.information(self, "Success", f"Tanaman '{data['name']}' berhasil ditambahkan!")
