import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QCompleter, QListView
)
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QColor

class AddPlantForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Add New Plant")
        self.setModal(True) 
        self.setFixedSize(450, 560) 
        
        # Styling global untuk Dialog
        self.setStyleSheet("background-color: white; border-radius: 12px;") 

        # CSS CSS UTAMA
        # Kita mendefinisikan logic warna langsung di sini menggunakan selector [is_placeholder="true"]
        self.main_stylesheet = """
            /* --- QLINEEDIT --- */
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #fcfcfc;
                font-size: 14px;
                color: #333;
                min-height: 30px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
                background-color: #ffffff;
            }

            /* --- QCOMBOBOX DEFAULT (Saat ada isinya) --- */
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #fcfcfc;
                font-size: 14px;
                min-height: 30px;
                color: #333; /* Warna Hitam Normal */
            }

            /* --- QCOMBOBOX PLACEHOLDER (Saat index 0) --- */
            /* Selector ini aktif jika kita setProperty('is_placeholder', True) */
            QComboBox[is_placeholder="true"] {
                color: #888;         /* Warna Abu-abu */
                font-style: italic;  /* Miring */
            }

            QComboBox:focus {
                border: 1px solid #4CAF50;
                background-color: #ffffff;
            }

            /* AREA PANAH */
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 0px;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            
            /* GAMBAR PANAH SVG */
            QComboBox::down-arrow {
                image: url(data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>);
                width: 14px;
                height: 14px;
            }

            /* ITEM LIST */
            QComboBox QAbstractItemView {
                border: 1px solid #ddd;
                background-color: white;
                selection-background-color: #f0f0f0;
                selection-color: #333;
                outline: none;
            }
        """

        self.init_ui()
        self.setup_species_completer()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # --- HEADER ---
        header_layout = QHBoxLayout()
        title_label = QLabel("Add New Plant")
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333;")
        
        close_button = QPushButton("x")
        close_button.setFixedSize(24, 24)
        close_button.setFont(QFont("Arial", 14))
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: #888;
            }
            QPushButton:hover {
                color: #555;
            }
        """)
        close_button.clicked.connect(self.reject)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        main_layout.addLayout(header_layout)

        # --- FORM INPUT ---
        form_widgets_layout = QVBoxLayout()
        form_widgets_layout.setSpacing(15)

        label_style = "color: #555; font-size: 13px; font-weight: bold;"
        
        def create_input_group(label_text, input_widget):
            group_layout = QVBoxLayout()
            group_layout.setSpacing(6)
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            
            # Terapkan stylesheet utama ke widget input
            input_widget.setStyleSheet(self.main_stylesheet)
            
            group_layout.addWidget(lbl)
            group_layout.addWidget(input_widget)
            return group_layout

        # A. Plant Name
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("e.g. My Monstera")
        form_widgets_layout.addLayout(create_input_group("Plant Name", self.input_name))

        # B. Species
        self.input_species = QLineEdit()
        self.input_species.setPlaceholderText("e.g. Monstera deliciosa")
        form_widgets_layout.addLayout(create_input_group("Species", self.input_species))

        # Helper Logic untuk Placeholder Dinamis
        def setup_combo_placeholder(combo, placeholder_text, items):
            model = QStandardItemModel()
            
            # 1. Item Placeholder (Warna abu-abu di list dropdown)
            item_placeholder = QStandardItem(placeholder_text)
            item_placeholder.setForeground(QColor("#888")) 
            item_placeholder.setSelectable(False)
            model.appendRow(item_placeholder)
            
            # 2. Item Pilihan
            for text in items:
                item = QStandardItem(text)
                item.setForeground(QColor("#333"))
                model.appendRow(item)
            
            combo.setModel(model)
            combo.setView(QListView())
            
            # 3. LOGIKA UPDATE PROPERTY
            # Ini fungsi yang akan dipanggil saat index berubah
            def update_style():
                is_placeholder = (combo.currentIndex() == 0)
                
                # Set properti kustom 'is_placeholder' ke True/False
                combo.setProperty("is_placeholder", is_placeholder)
                
                # PENTING: Paksa Qt untuk memuat ulang style berdasarkan properti baru
                combo.style().unpolish(combo)
                combo.style().polish(combo)

            # Hubungkan sinyal
            combo.currentIndexChanged.connect(update_style)
            
            # Set awal
            combo.setCurrentIndex(0)
            update_style() # Panggil sekali di awal untuk set warna abu-abu

        # C. Growing Media
        self.combo_media = QComboBox()
        media_items = ["Soil", "Water (Hydroponic)", "Leca", "Sphagnum Moss", "Coco Coir"]
        # Pasang ke layout dulu agar style bisa diaplikasikan
        group_media = create_input_group("Growing Media", self.combo_media)
        form_widgets_layout.addLayout(group_media)
        # Baru setup logic placeholder
        setup_combo_placeholder(self.combo_media, "Pick Growing Media...", media_items)

        # D. Sunlight Habit
        self.combo_sun = QComboBox()
        sun_items = [
            "Full Sun (6+ hours direct sun)",
            "Partial Sun (3-6 hours direct sun)",
            "Indirect Light (Bright, no direct sun)",
            "Shade (< 3 hours direct sun)",
            "Low Light (Artificial/Dim)"
        ]
        group_sun = create_input_group("Sunlight Habit", self.combo_sun)
        form_widgets_layout.addLayout(group_sun)
        setup_combo_placeholder(self.combo_sun, "Pick Sunlight Habit...", sun_items)

        main_layout.addLayout(form_widgets_layout)
        main_layout.addStretch()

        # --- TOMBOL AKSI ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setFixedSize(120, 45)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_add = QPushButton("Add Plant")
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setFixedSize(120, 45)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #1E6F26;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #165a1d;
            }
        """)
        self.btn_add.clicked.connect(self.on_save_clicked)

        btn_layout.addStretch() 
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_add)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def setup_species_completer(self):
        species_list = [
            "Monstera deliciosa", "Monstera adansonii", "Epipremnum aureum (Golden Pothos)", 
            "Sansevieria trifasciata", "Ficus lyrata (Fiddle-leaf Fig)", "Zamioculcas zamiifolia (ZZ Plant)", 
            "Calathea orbifolia", "Philodendron 'Pink Princess'", "Aloe vera", "Opuntia microdasys"
        ]
        completer = QCompleter(species_list, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.input_species.setCompleter(completer)

    def on_save_clicked(self):
        nama = self.input_name.text().strip()
        species = self.input_species.text().strip()
        
        if not nama:
            QMessageBox.warning(self, "Input Error", "Plant Name tidak boleh kosong!")
            return
        if not species:
            QMessageBox.warning(self, "Input Error", "Species tidak boleh kosong!")
            return
            
        if self.combo_media.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Silakan pilih Growing Media!")
            return
            
        if self.combo_sun.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Silakan pilih Sunlight Habit!")
            return

        self.accept()

    def get_data(self):
        full_sunlight_text = self.combo_sun.currentText()
        clean_sunlight = full_sunlight_text.split(" (")[0]

        return {
            "name": self.input_name.text().strip(),
            "species": self.input_species.text().strip(),
            "media": self.combo_media.currentText(),
            "sunlight_habit": clean_sunlight,
        }