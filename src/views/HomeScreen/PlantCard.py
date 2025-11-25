from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor


class PlantCard(QFrame):
    deleteRequested = pyqtSignal(str)
    detailsRequested = pyqtSignal(str)

    def __init__(self, plant_id, name, sci_name, stats, action_text=None):
        super().__init__()
        self.plant_id = plant_id
        self.setProperty("class", "plant-card")
        self.setStyleSheet("background-color: white; border-radius: 12px;")
        self.setFixedSize(350, 430)

        self.btn_delete = QPushButton("🗑️", self)
        self.btn_delete.setFixedSize(50, 50)
        self.btn_delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_delete.setToolTip("Remove Plant")
        
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #ddd;
                border-radius: 25px;
                font-size: 18px;
                color: #555;
            }
            QPushButton:hover {
                background-color: #ffebee; /* Merah muda pudar saat hover */
                color: #d32f2f;
                border: 1px solid #d32f2f;
            }
        """)
        self.btn_delete.clicked.connect(self.emit_delete_signal)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        img_placeholder = QLabel("🌿")
        img_placeholder.setAlignment(Qt.AlignCenter)
        img_placeholder.setStyleSheet("background-color: #EEEEEE; border-radius: 8px; font-size: 40px;")
        img_placeholder.setFixedHeight(120)
        layout.addWidget(img_placeholder)
        
        title_lbl = QLabel(name)
        title_lbl.setStyleSheet("font-weight: bold; font-size: 20px;")
        sub_lbl = QLabel(sci_name)
        sub_lbl.setStyleSheet("color: gray; font-size: 16px; font-style: italic; margin-bottom: 7px;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(sub_lbl)
        
        stats_items = list(stats.items()) 
        
        lbl_style = """
            QLabel {
                color: #555; 
                background-color: #F5F5F5; 
                padding: 6px 8px; 
                border-radius: 6px;
                font-weight: bold;
            }
        """

        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(8)
        row1_layout.setContentsMargins(0, 0, 0, 0)
        
        if len(stats_items) > 0:
            icon, val = stats_items[0]
            lbl = QLabel(f"{icon} {val}")
            lbl.setStyleSheet(lbl_style)
            lbl.setAlignment(Qt.AlignCenter) 
            
            row1_layout.addWidget(lbl, 1) 

        layout.addLayout(row1_layout)

        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(8)
        row2_layout.setContentsMargins(0, 4, 0, 0)
        
        for i in range(1, 3): 
            if i < len(stats_items):
                icon, val = stats_items[i]
                lbl = QLabel(f"{icon} {val}")
                lbl.setStyleSheet(lbl_style)
                lbl.setAlignment(Qt.AlignCenter)
                row2_layout.addWidget(lbl, 1) 
        
        layout.addLayout(row2_layout)

        row3_layout = QHBoxLayout()
        row3_layout.setSpacing(8)
        row3_layout.setContentsMargins(0, 4, 0, 0)
        
        for i in range(3, 5): 
            if i < len(stats_items):
                icon, val = stats_items[i]
                lbl = QLabel(f"{icon} {val}")
                lbl.setStyleSheet(lbl_style)
                lbl.setAlignment(Qt.AlignCenter)
                row3_layout.addWidget(lbl, 1)
        
        layout.addLayout(row3_layout)

        layout.addStretch()
        
        btn = QPushButton(action_text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            /* State Normal */
            QPushButton {
                background-color: #E3F2FD; 
                color: #1976D2; 
                border: none; 
                border-radius: 6px; 
                padding: 10px; 
                font-weight: bold;
            }
            
            /* State Hover (Saat mouse di atas tombol) */
            QPushButton:hover {
                background-color: #BBDEFB; /* Warna biru muda yang sedikit lebih gelap */
                color: #1565C0;            /* Warna teks sedikit lebih tajam */
            }

            /* State Pressed (Opsional: Saat tombol ditekan) */
            QPushButton:pressed {
                background-color: #90CAF9; /* Lebih gelap lagi */
                padding-top: 11px;         /* Efek tombol "mendelep" sedikit */
                padding-bottom: 9px;
            }
        """)
        layout.addWidget(btn)
        btn.clicked.connect(self.emit_details_signal)
            
        self.setLayout(layout)
    
    def resizeEvent(self, event):
        """
        Dipanggil otomatis saat widget digambar/diubah ukurannya.
        Memastikan tombol selalu di pojok kanan atas & DI ATAS widget lain.
        """
        super().resizeEvent(event)
        self.btn_delete.move(self.width() - 60, 10)
        self.btn_delete.raise_()

    def emit_delete_signal(self):
        self.deleteRequested.emit(self.plant_id)

    def emit_details_signal(self):
        self.detailsRequested.emit(self.plant_id)