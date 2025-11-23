import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, 
    QCompleter, QListView, QSpinBox, QDateEdit, QWidget, QSizePolicy, QScrollArea,
)
from PyQt5.QtCore import Qt, QStringListModel, QDate, QEvent, QObject
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QColor


class NoScrollEventFilter(QObject):
    """Event filter to prevent mouse wheel from modifying spinbox/combobox values"""
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            if isinstance(obj, (QSpinBox, QDateEdit, QComboBox)):
                return True  # Consume the wheel event
        return super().eventFilter(obj, event)


class AddPlantForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Add New Plant")
        self.setModal(True) 
        # allow resizing and use minimum size so long forms can scroll
        self.setMinimumSize(450, 600)
        
        self.setStyleSheet("background-color: white; border-radius: 12px;") 

        # --- CSS UTAMA (FIXED: Simplified QComboBox styling to prevent parsing errors) ---
        self.main_stylesheet = """
            QLineEdit, QSpinBox, QDateEdit { 
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #fcfcfc;
                font-size: 14px;
                color: #333;
                min-height: 30px;
            }
            QLineEdit:focus, QSpinBox:focus, QDateEdit:focus {
                border: 1px solid #4CAF50;
                background-color: #ffffff;
            }

            QComboBox {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #fcfcfc;
                font-size: 14px;
                min-height: 30px; 
                color: #333; 
            }

            QComboBox[is_placeholder="true"] {
                color: #888;         
                font-style: italic;  
            }

            QComboBox:focus {
                border: 1px solid #4CAF50;
                background-color: #ffffff;
            }

            /* Simplified dropdown area, removed complex SVG to fix parsing */
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px; /* Reduced width */
                border-left-width: 1px; /* Added separator */
                border-left-color: #ddd;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            
            /* REMOVED: QComboBox::down-arrow with SVG image that caused parsing errors */
            /* Qt will use its default arrow icon now, which is safer. */

            QComboBox QAbstractItemView {
                border: 1px solid #ddd;
                background-color: white;
                selection-background-color: #f0f0f0;
                selection-color: #333;
                outline: none;
            }
        """
        
        # Calendar styling for date picker (black month/year text)
        self.calendar_stylesheet = """
            QCalendarWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QCalendarWidget QWidget { 
                background-color: white;
                color: #000;
            }
            QCalendarWidget QToolButton {
                color: #000;
                background-color: #f5f5f5;
                border: none;
                border-radius: 4px;
                padding: 4px;
                margin: 2px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #e0e0e0;
            }
            QCalendarWidget QMenu {
                color: #000;
                background-color: white;
                border: 1px solid #ddd;
            }
            QCalendarWidget QMenu::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """

        self.scroll_filter = NoScrollEventFilter()
        self.init_ui()
        self.setup_species_completer()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

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
        # FIX: Increased main vertical spacing to 18px
        form_widgets_layout.setSpacing(18) 

        label_style = "color: #555; font-size: 13px; font-weight: bold;"
        
        def create_input_group(label_text, input_widget):
            container = QWidget()
            group_layout = QVBoxLayout(container)
            group_layout.setSpacing(6)
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)

            # Apply stylesheet
            if isinstance(input_widget, (QLineEdit, QSpinBox, QDateEdit, QComboBox)):
                input_widget.setStyleSheet(self.main_stylesheet)
                # Install event filter to prevent scroll wheel from modifying values
                input_widget.installEventFilter(self.scroll_filter)

            # Ensure inputs have a sensible size policy to avoid overlapping
            try:
                input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            except Exception:
                pass

            group_layout.addWidget(lbl)
            group_layout.addWidget(input_widget)
            return container

        # 1. Plant Name
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("e.g. My Kitchen Basil")
        form_widgets_layout.addWidget(create_input_group("Plant Name / Nickname", self.input_name))

        # 2. Species (Auto-complete)
        self.input_species = QLineEdit()
        self.input_species.setPlaceholderText("Start typing (e.g. Monstera...)")
        form_widgets_layout.addWidget(create_input_group("Species", self.input_species))

        # 3. Age & Date (The Hybrid Approach)
        stats_layout = QVBoxLayout()
        # FIX: Increased spacing between Date Acquired and Age/Height row to 30px
        stats_layout.setSpacing(30) 

        # Row A: Date Acquired (The Anchor)
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate()) # Default to Today
        self.input_date.setDisplayFormat("yyyy-MM-dd")
        self.input_date.calendarWidget().setStyleSheet(self.calendar_stylesheet)
        stats_layout.addWidget(create_input_group("Date Acquired/Planted", self.input_date))

        # Row B: Initial Age & Height (Side by Side)
        row_measurements = QHBoxLayout()
        row_measurements.setSpacing(15)

        # Initial Age (The Offset)
        self.input_initial_age = QSpinBox()
        self.input_initial_age.setRange(0, 240) 
        self.input_initial_age.setSuffix(" months old")
        self.input_initial_age.setToolTip("How old was the plant when you got it? (Estimate)")
        row_measurements.addWidget(create_input_group("Est. Age at Acquisition", self.input_initial_age))

        # Height
        self.input_height = QSpinBox()
        self.input_height.setRange(0, 1000) 
        self.input_height.setSuffix(" cm")
        row_measurements.addWidget(create_input_group("Current Height", self.input_height))
        
        stats_layout.addLayout(row_measurements)
        
        form_widgets_layout.addLayout(stats_layout)

        # Helper Logic for ComboBox Placeholders
        def setup_combo_placeholder(combo, placeholder_text, items):
            model = QStandardItemModel()
            item_placeholder = QStandardItem(placeholder_text)
            item_placeholder.setForeground(QColor("#888")) 
            item_placeholder.setSelectable(False)
            model.appendRow(item_placeholder)
            
            for text in items:
                item = QStandardItem(text)
                item.setForeground(QColor("#333"))
                model.appendRow(item)
            
            combo.setModel(model)
            combo.setView(QListView())
            
            def update_style():
                is_placeholder = (combo.currentIndex() == 0)
                combo.setProperty("is_placeholder", is_placeholder)
                combo.style().unpolish(combo)
                combo.style().polish(combo)

            combo.currentIndexChanged.connect(update_style)
            combo.setCurrentIndex(0)
            update_style()

        # 4. Growing Media
        self.combo_media = QComboBox()
        media_items = ["Soil", "Water (Hydroponic)", "Leca", "Sphagnum Moss", "Coco Coir"]
        form_widgets_layout.addWidget(create_input_group("Growing Media", self.combo_media))
        setup_combo_placeholder(self.combo_media, "Select Media...", media_items)

        # 5. Sunlight Habit
        self.combo_sun = QComboBox()
        sun_items = [
            "Full Sun (6+ hours direct sun)",
            "Partial Sun (3-6 hours direct sun)",
            "Indirect Light (Bright, no direct sun)",
            "Shade (< 3 hours direct sun)",
            "Low Light (Artificial/Dim)"
        ]
        form_widgets_layout.addWidget(create_input_group("Placement / Sunlight", self.combo_sun))
        setup_combo_placeholder(self.combo_sun, "Select Sunlight...", sun_items)

        # 6. Initial Leaf Color (For initial diagnostics)
        self.combo_color = QComboBox()
        color_items = ["Green", "Yellow", "Brown/Crispy", "Pale/Faded", "Black/Mushy"]
        form_widgets_layout.addWidget(create_input_group("Current Leaf Condition", self.combo_color))
        setup_combo_placeholder(self.combo_color, "Select Leaf Color...", color_items)

        # Wrap the form widgets in a scroll area to avoid overflow/hiding (only form scrolls, buttons stay fixed)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")
        scroll_content = QWidget()
        scroll_content.setLayout(form_widgets_layout)
        scroll.setWidget(scroll_content)

        main_layout.addWidget(scroll, 1)  # Give scroll area stretch factor

        # --- BUTTONS (Fixed at bottom, not scrollable) ---
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

        main_layout.addLayout(btn_layout, 0)  # Add buttons with no stretch (fixed position)
        self.setLayout(main_layout)

    def setup_species_completer(self):
        """Fetches species list from SQLite database for auto-complete"""
        species_list = []
        
        # Calculate the absolute path to the database
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', '..', 'data', 'plants.db')
        db_path = os.path.normpath(db_path)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT common_name FROM species")
            rows = cursor.fetchall()
            species_list = [row[0] for row in rows]
            conn.close()
        except sqlite3.Error as e:
            print(f"Database Error (Path: {db_path}): {e}")
            species_list = ["Snake Plant", "Monstera", "Pothos", "Aloe Vera"]

        completer = QCompleter(species_list, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.input_species.setCompleter(completer)

    def on_save_clicked(self):
        # Validation
        nama = self.input_name.text().strip()
        species = self.input_species.text().strip()
        
        if not nama:
            QMessageBox.warning(self, "Input Error", "Plant Name cannot be empty!")
            return
        if not species:
            QMessageBox.warning(self, "Input Error", "Species cannot be empty!")
            return
        if self.combo_media.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select Growing Media!")
            return
        if self.combo_sun.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select Sunlight Habit!")
            return
        if self.combo_color.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select Current Leaf Condition!")
            return

        self.accept()

    def get_data(self):
        """
        Returns the dictionary of data to be used by the main logic.
        FIX: Includes the old keys ('name', 'species', 'media', 'sunlight_habit') 
             for backward compatibility.
        """
        date_acquired_str = self.input_date.date().toString("yyyy-MM-dd")
        nickname = self.input_name.text().strip()
        species = self.input_species.text().strip()
        media = self.combo_media.currentText()
        # Ambil nilai sunlight
        sunlight = self.combo_sun.currentText() 

        return {
            # FIX: Included old keys for backward compatibility
            "name": nickname,           
            "species": species,
            "media": media,
            "sunlight_habit": sunlight, # <--- PERBAIKAN BARU
            
            # New, more descriptive keys
            "plant_nickname": nickname,
            "species_name": species,
            "growing_media": media,
            "sunlight_condition": sunlight,
            
            "date_acquired": date_acquired_str,
            "initial_age_months": self.input_initial_age.value(),
            "current_height_cm": self.input_height.value(),
            "current_leaf_color": self.combo_color.currentText()
        }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = AddPlantForm()
    if form.exec_() == QDialog.Accepted:
        print(form.get_data())
    sys.exit(app.exec_())