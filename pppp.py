from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QFormLayout, QComboBox
import sys
from datetime import datetime
class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Age Calculator')
        grid = QGridLayout()
        name_label = QLabel('Enter your name:')
        self.name_line_edit = QLineEdit()
        date_birth_label = QLabel('Enter your Date of Birth MM/DD/YYYY:')
        #make it instance variable - add self 
        self.date_birth_line_edit = QLineEdit()
        
        calculate_button = QPushButton('Calculate')
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel('Your age is: ')

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_birth_label, 1, 0)
        grid.addWidget(self.date_birth_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0,1,2)
        #span across 2 columns and in 3rd row
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        date_of_birth = self.date_birth_line_edit.text()
        age = current_year - int(date_of_birth[-4:])
        self.output_label.setText(f'{self.name_line_edit.text()} is {age} years old.')


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())