import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QGroupBox, QRadioButton, QLineEdit, QLabel, QPushButton, QFormLayout, QHBoxLayout
)
from PyQt5.QtGui import QDoubleValidator, QFont
from PyQt5.QtCore import Qt

class ResistanceCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resistance for Printed Protopasta")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Create the tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Add the "Protopasta" tab
        protopasta_tab = QWidget()
        tab_widget.addTab(protopasta_tab, "Printed Protopasta")

        # Set up the layout for the Protopasta tab
        tab_layout = QVBoxLayout()
        protopasta_tab.setLayout(tab_layout)

        # Resistivity selection group
        resistivity_group = QGroupBox("Select Resistivity")
        resistivity_layout = QHBoxLayout()
        resistivity_group.setLayout(resistivity_layout)

        self.radio_xy = QRadioButton("X/Y Resistivity (30 Ω.cm)")
        self.radio_z = QRadioButton("Z Resistivity (115 Ω·cm)")
        self.radio_xy.setChecked(True)

        resistivity_layout.addWidget(self.radio_xy)
        resistivity_layout.addWidget(self.radio_z)

        # Unknown variable selection group
        unknown_group = QGroupBox("Unknown to Calculate")
        unknown_layout = QHBoxLayout()
        unknown_group.setLayout(unknown_layout)

        self.radio_resistance = QRadioButton("Resistance (R)")
        self.radio_length = QRadioButton("Length (L)")
        self.radio_area = QRadioButton("Area (A)")
        self.radio_resistance.setChecked(True)

        unknown_layout.addWidget(self.radio_resistance)
        unknown_layout.addWidget(self.radio_length)
        unknown_layout.addWidget(self.radio_area)

        # Input fields
        input_group = QGroupBox("Input Known Values")
        input_layout = QFormLayout()
        input_group.setLayout(input_layout)

        self.input_resistance = QLineEdit()
        self.input_length = QLineEdit()
        self.input_area = QLineEdit()

        # Validators to ensure only numbers are entered
        validator = QDoubleValidator(0.0, 1e9, 4)
        self.input_resistance.setValidator(validator)
        self.input_length.setValidator(validator)
        self.input_area.setValidator(validator)

        # Add units to the labels
        input_layout.addRow("Resistance (Ω):", self.input_resistance)
        input_layout.addRow("Length (cm):", self.input_length)
        input_layout.addRow("Area (cm²):", self.input_area)

        # Disable the input field for the unknown variable
        self.input_resistance.setDisabled(True)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setFixedWidth(150)

        # Result display
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        result_font = QFont("Segoe UI", 12, QFont.Bold)
        self.result_label.setFont(result_font)

        # Add widgets to the tab layout
        tab_layout.addWidget(resistivity_group)
        tab_layout.addWidget(unknown_group)
        tab_layout.addWidget(input_group)
        tab_layout.addWidget(self.calculate_button, alignment=Qt.AlignCenter)
        tab_layout.addWidget(self.result_label)

        # Connect signals and slots
        self.radio_resistance.toggled.connect(self.update_unknown)
        self.radio_length.toggled.connect(self.update_unknown)
        self.radio_area.toggled.connect(self.update_unknown)
        self.calculate_button.clicked.connect(self.calculate)

        # Style the application
        self.apply_styles()

    def update_unknown(self):
        # Enable all inputs first
        self.input_resistance.setEnabled(True)
        self.input_length.setEnabled(True)
        self.input_area.setEnabled(True)

        # Disable the input corresponding to the selected unknown
        if self.radio_resistance.isChecked():
            self.input_resistance.clear()
            self.input_resistance.setDisabled(True)
        elif self.radio_length.isChecked():
            self.input_length.clear()
            self.input_length.setDisabled(True)
        elif self.radio_area.isChecked():
            self.input_area.clear()
            self.input_area.setDisabled(True)

    def calculate(self):
        try:
            # Select resistivity based on user choice
            if self.radio_xy.isChecked():
                resistivity = 30  # Ω·mm²/m
            else:
                resistivity = 115  # Ω·mm²/m

            # Perform calculation based on the unknown variable
            if self.radio_resistance.isChecked():
                length = float(self.input_length.text())
                area = float(self.input_area.text())
                resistance = (resistivity * length) / area
                result = f"Resistance (R) = {resistance:.4f} Ω"
            elif self.radio_length.isChecked():
                resistance = float(self.input_resistance.text())
                area = float(self.input_area.text())
                length = (resistance * area) / resistivity
                result = f"Length (L) = {length:.4f} cm"
            elif self.radio_area.isChecked():
                resistance = float(self.input_resistance.text())
                length = float(self.input_length.text())
                area = (resistivity * length) / resistance
                result = f"Area (A) = {area:.4f} cm²"
            else:
                result = "Please select an unknown variable."

            self.result_label.setText(result)
        except ValueError:
            self.result_label.setText("Please enter valid numeric values.")
        except ZeroDivisionError:
            self.result_label.setText("Error: Division by zero.")
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

    def apply_styles(self):
        # Apply styles to the application
        style = """
        QWidget {
            font-family: 'Segoe UI';
            font-size: 10pt;
            color: #333;
        }
        QMainWindow {
            background-color: #f0f0f0;
        }
        QGroupBox {
            background-color: #fafafa;
            border: 1px solid #dcdcdc;
            border-radius: 5px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            color: #555;
        }
        QLabel {
            font-size: 10pt;
        }
        QLineEdit {
            background-color: #fff;
            border: 1px solid #ccc;
            padding: 5px;
            border-radius: 3px;
        }
        QLineEdit:disabled {
            background-color: #e6e6e6;
        }
        QPushButton {
            background-color: #007acc;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            font-size: 10pt;
        }
        QPushButton:hover {
            background-color: #005f99;
        }
        QRadioButton {
            font-size: 10pt;
        }
        QLabel#result_label {
            font-size: 12pt;
            font-weight: bold;
            color: #007acc;
            margin-top: 10px;
        }
        """
        self.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResistanceCalculator()
    window.show()
    sys.exit(app.exec_())
