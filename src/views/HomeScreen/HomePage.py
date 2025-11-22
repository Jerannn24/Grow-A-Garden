import time
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QMessageBox, QDialog
from PyQt5.QtCore import Qt, pyqtSignal

from controllers.PlantManager import PlantManager
from views.AddPlantForm import AddPlantForm
from views.RemovePlantForm import RemovePlantForm
from .PlantCard import PlantCard
from .AddPlantCard import AddPlantCard
from .FlowLayout import FlowLayout

class HomePage(QWidget):
    openDetailRequested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.plant_manager = PlantManager()
        self.current_user_id = None
        # Load data awal dari DB ke memory
        self.plant_manager.loadUserData(self.current_user_id) 

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(10)
                
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        self.content_widget = QWidget()
        self.flow_layout = FlowLayout(self.content_widget) 
        self.flow_layout.setSpacing(20)
        self.scroll.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll)

        self.refresh_plant_list()

    def refresh_plant_list(self):
        
        if not self.current_user_id:
            return
        
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        add_card = AddPlantCard()
        add_card.clicked.connect(self.open_add_plant_form)
        self.flow_layout.addWidget(add_card)

        # Ambil Data dari manager
        plants = self.plant_manager.plantList 

        for plant in plants:
            p_id = plant.getPlantID()
            p_name = plant.getPlantName()
            p_species = plant.getPlantSpecies()
            p_media = plant.getPlantMedia()
            p_sun = plant.getLightingDuration() 
            p_water = plant.getWateringFrequency()
            p_phase = plant.getPlantPhase()
            p_harvest = plant.getHarvestEstim()

            stats = {"🌱": p_media, "🔄": p_phase, "📅": p_harvest, "☀️": p_sun, "💧": p_water}
            
            card = PlantCard(
                plant_id=p_id,
                name=p_name,
                sci_name=p_species,
                stats=stats,
                action_text="Details",
            )
            card.deleteRequested.connect(self.handle_delete_plant)
            card.detailsRequested.connect(self.openDetailRequested.emit)
            self.flow_layout.addWidget(card)
                
    def set_current_user_id(self, userID: int):
        if self.current_user_id != userID:
            self.current_user_id = userID
            self.plant_manager.loadUserData(self.current_user_id)
            self.refresh_plant_list()
    
    def open_add_plant_form(self):
        if not self.current_user_id:
             QMessageBox.critical(self, "Error", "UserID belum terdeteksi. Silakan login ulang.")
             return
         
        form = AddPlantForm(self)
        
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            
            data['userID'] = self.current_user_id
            data['plantID'] = f"P{int(time.time())}" 
            data['date'] = datetime.now().strftime('%Y-%m-%d')
            
            print("Debug: Mengirim data ke Manager:", data)

            self.plant_manager.onAddClick(data) 
            self.refresh_plant_list()
            
            QMessageBox.information(self, "Success", f"Tanaman '{data['name']}' berhasil ditambahkan!")

    def handle_delete_plant(self, plant_id):
            target_plant = next((p for p in self.plant_manager.plantList if p.plantID == plant_id), None)
            
            if target_plant:
                dialog = RemovePlantForm(target_plant.getPlantName(), self)
                
                if dialog.exec_() == QDialog.Accepted:
                    success = self.plant_manager.onDeleteClick(plant_id)
                    
                    if success:
                        self.refresh_plant_list()