from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QComboBox, QListView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QStandardItemModel, QStandardItem, QColor
from models.Plant import Plant


class PlantGrowthForm(QDialog):
    """Dialog that records the latest height and leaf color for a plant."""

    confirmed = pyqtSignal(int, str)

    def __init__(self, task=None, parent=None):
        super().__init__(parent)
        self.task = task
        self.plant_id = getattr(task, 'plantID', None)
        self.setWindowTitle("Update Plant Growth")
        self.setModal(True)
        self.setFixedWidth(420)
        self.setStyleSheet(
            """
            QDialog { background-color: white; border-radius: 12px; }
            QLabel#Title { font-size: 20px; font-weight: bold; color: #1B5E20; }
            QLabel#Desc { color: #555; font-size: 13px; }
            QLabel#Label { font-size: 13px; color: #333; font-weight: bold; }
            QLabel#Error { color: #D32F2F; font-size: 12px; }
            QSpinBox, QComboBox {
                border: 1px solid #DDD;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QSpinBox:focus, QComboBox:focus {
                border: 2px solid #2E7D32;
            }
            QComboBox[is_placeholder="true"] { color: #888; font-style: italic; }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 20px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QPushButton {
                border-radius: 8px;
                font-weight: bold;
                height: 40px;
            }
            QPushButton#Confirm {
                background-color: #2E7D32;
                color: white;
                border: none;
            }
            QPushButton#Confirm:hover {
                background-color: #1B5E20;
            }
            QPushButton#Cancel {
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #DDD;
            }
            QPushButton#Cancel:hover {
                background-color: #EEEEEE;
            }
            """
        )

        self._build_ui()
        self._load_existing_values()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(14)

        title = QLabel("Record Plant Growth")
        title.setObjectName("Title")
        layout.addWidget(title)

        desc = QLabel("Log the latest plant height and dominant leaf color to keep history up to date.")
        desc.setWordWrap(True)
        desc.setObjectName("Desc")
        layout.addWidget(desc)

        lbl_height = QLabel("Current Height (cm)")
        lbl_height.setObjectName("Label")
        layout.addWidget(lbl_height)

        self.height_input = QSpinBox()
        self.height_input.setRange(0, 1000)
        self.height_input.setSuffix(" cm")
        layout.addWidget(self.height_input)

        lbl_color = QLabel("Leaf Color")
        lbl_color.setObjectName("Label")
        layout.addWidget(lbl_color)

        self.leaf_combo = QComboBox()
        self._setup_color_dropdown()
        layout.addWidget(self.leaf_combo)

        self.error_label = QLabel()
        self.error_label.setObjectName("Error")
        self.error_label.setVisible(False)
        layout.addWidget(self.error_label)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("Cancel")
        btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        self.btn_confirm = QPushButton("Save Update")
        self.btn_confirm.setObjectName("Confirm")
        self.btn_confirm.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_confirm.setDefault(True)
        self.btn_confirm.setAutoDefault(True)
        self.btn_confirm.clicked.connect(self._on_confirm)

        button_row.addWidget(btn_cancel)
        button_row.addWidget(self.btn_confirm)
        layout.addLayout(button_row)

    def _load_existing_values(self):
        if not self.plant_id:
            return
        try:
            conn = Plant._get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT height, leafColor FROM plants WHERE plantID = ?", (self.plant_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                height_value = row[0] if isinstance(row, tuple) else row['height']
                leaf_color = row[1] if isinstance(row, tuple) else row['leafColor']
                if height_value is not None:
                    try:
                        self.height_input.setValue(int(round(float(height_value))))
                    except Exception:
                        pass
                if leaf_color:
                    self._select_leaf_color(str(leaf_color))
        except Exception as exc:
            print(f"[PlantGrowthForm] Failed to load plant data: {exc}")

    def _on_confirm(self):
        if not self.plant_id:
            self._show_error("Plant ID is missing, unable to save.")
            return

        height = int(self.height_input.value())

        if self.leaf_combo.currentIndex() <= 0:
            self._show_error("Please select a leaf color.")
            return

        leaf_color = self.leaf_combo.currentText()

        try:
            conn = Plant._get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE plants SET height = ?, leafColor = ? WHERE plantID = ?",
                (height, leaf_color, self.plant_id)
            )
            conn.commit()
            conn.close()
        except Exception as exc:
            self._show_error(f"Failed to save data: {exc}")
            return

        self.error_label.setVisible(False)
        self.confirmed.emit(height, leaf_color)
        self.accept()

    def _show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self._on_confirm()
            return
        super().keyPressEvent(event)

    def _setup_color_dropdown(self):
        """Populate the leaf color dropdown with AddPlant-style placeholder behavior."""
        self._color_options = [
            "Green",
            "Yellow",
            "Brown/Crispy",
            "Pale/Faded",
            "Black/Mushy"
        ]

        model = QStandardItemModel()
        placeholder = QStandardItem("Select leaf color...")
        placeholder.setForeground(QColor("#888"))
        placeholder.setSelectable(False)
        model.appendRow(placeholder)

        for text in self._color_options:
            item = QStandardItem(text)
            item.setForeground(QColor("#333"))
            model.appendRow(item)

        self.leaf_model = model
        self.leaf_combo.setModel(model)
        self.leaf_combo.setView(QListView())
        self.leaf_combo.setCurrentIndex(0)
        self._update_combo_placeholder_state()
        self.leaf_combo.currentIndexChanged.connect(lambda _: self._update_combo_placeholder_state())

    def _update_combo_placeholder_state(self):
        is_placeholder = self.leaf_combo.currentIndex() == 0
        self.leaf_combo.setProperty("is_placeholder", is_placeholder)
        self.leaf_combo.style().unpolish(self.leaf_combo)
        self.leaf_combo.style().polish(self.leaf_combo)

    def _select_leaf_color(self, color_text: str):
        idx = self.leaf_combo.findText(color_text, Qt.MatchFixedString)
        if idx != -1:
            self.leaf_combo.setCurrentIndex(idx)
            return

        item = QStandardItem(color_text)
        item.setForeground(QColor("#333"))
        self.leaf_model.appendRow(item)
        self.leaf_combo.setCurrentIndex(self.leaf_model.rowCount() - 1)
