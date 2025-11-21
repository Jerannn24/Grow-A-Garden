from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt


class PlantCard(QFrame):
    def __init__(self, name, sci_name, stats, action_text=None, warning=None):
        super().__init__()
        self.setProperty("class", "plant-card")
        self.setStyleSheet("background-color: white; border-radius: 12px;")
        self.setFixedSize(350, 430)
        
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
        
        if warning:
            warn_lbl = QLabel(warning)
            warn_lbl.setAlignment(Qt.AlignCenter)
            warn_lbl.setStyleSheet("background-color: #FFF9C4; color: #FBC02D; padding: 8px; border-radius: 6px; font-weight: bold;")
            layout.addWidget(warn_lbl)
        elif action_text:
            btn = QPushButton(action_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("background-color: #E3F2FD; color: #1976D2; border: none; border-radius: 6px; padding: 10px; font-weight: bold;")
            layout.addWidget(btn)
            
        self.setLayout(layout)
