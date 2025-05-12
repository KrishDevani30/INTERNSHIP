# FOR RUN THIS CODE GO TO TERMINAL AND RUN PROMPT:
# python .\sample_gui.py

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QLineEdit, 
                            QPushButton, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class SampleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sample GUI Application")
        self.showMaximized()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create header
        header = QFrame()
        header.setStyleSheet("background-color: #2c3e50; padding: 15px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_label = QLabel("Sample GUI Application")
        header_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(header_label)
        main_layout.addWidget(header)
        
        # Create navbar with dropdowns
        navbar = QFrame()
        navbar.setStyleSheet("background-color: #34495e; padding: 10px;")
        navbar_layout = QHBoxLayout(navbar)
        navbar_layout.setContentsMargins(20, 5, 20, 5)
        navbar_layout.setSpacing(20)
        
        # Style for all dropdowns
        dropdown_style = """
            QComboBox {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px;
                min-width: 150px;
                min-height: 25px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2c3e50;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #3498db;
                selection-color: white;
                border: 1px solid #bdc3c7;
                font-size: 14px;
            }
        """
        
        # First dropdown with nested dropdowns
        category_label = QLabel("Category:")
        category_label.setStyleSheet("color: white; font-size: 14px;")
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(dropdown_style)
        self.category_combo.addItems(["Electronics", "Clothing", "Food", "Books"])
        self.category_combo.currentIndexChanged.connect(self.update_subcategory)
        
        subcategory_label = QLabel("Subcategory:")
        subcategory_label.setStyleSheet("color: white; font-size: 14px;")
        self.subcategory_combo = QComboBox()
        self.subcategory_combo.setStyleSheet(dropdown_style)
        
        # Second dropdown with nested dropdowns
        location_label = QLabel("Location:")
        location_label.setStyleSheet("color: white; font-size: 14px;")
        self.location_combo = QComboBox()
        self.location_combo.setStyleSheet(dropdown_style)
        self.location_combo.addItems(["North", "South", "East", "West"])
        self.location_combo.currentIndexChanged.connect(self.update_city)
        
        city_label = QLabel("City:")
        city_label.setStyleSheet("color: white; font-size: 14px;")
        self.city_combo = QComboBox()
        self.city_combo.setStyleSheet(dropdown_style)
        
        # Third dropdown with nested dropdowns
        department_label = QLabel("Department:")
        department_label.setStyleSheet("color: white; font-size: 14px;")
        self.department_combo = QComboBox()
        self.department_combo.setStyleSheet(dropdown_style)
        self.department_combo.addItems(["IT", "HR", "Finance", "Marketing"])
        self.department_combo.currentIndexChanged.connect(self.update_team)
        
        team_label = QLabel("Team:")
        team_label.setStyleSheet("color: white; font-size: 14px;")
        self.team_combo = QComboBox()
        self.team_combo.setStyleSheet(dropdown_style)
        
        # Add all dropdowns to navbar
        navbar_layout.addWidget(category_label)
        navbar_layout.addWidget(self.category_combo)
        navbar_layout.addWidget(subcategory_label)
        navbar_layout.addWidget(self.subcategory_combo)
        navbar_layout.addWidget(location_label)
        navbar_layout.addWidget(self.location_combo)
        navbar_layout.addWidget(city_label)
        navbar_layout.addWidget(self.city_combo)
        navbar_layout.addWidget(department_label)
        navbar_layout.addWidget(self.department_combo)
        navbar_layout.addWidget(team_label)
        navbar_layout.addWidget(self.team_combo)
        navbar_layout.addStretch()
        
        main_layout.addWidget(navbar)
        
        # Create name section
        name_frame = QFrame()
        name_frame.setStyleSheet("background-color: #ecf0f1; padding: 15px;")
        name_layout = QHBoxLayout(name_frame)
        name_layout.setContentsMargins(20, 10, 20, 10)
        name_label = QLabel("Name:")
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        name_input = QLineEdit()
        name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                font-size: 14px;
                min-width: 200px;
            }
        """)
        name_input.setPlaceholderText("Enter your name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_input)
        name_layout.addStretch()
        main_layout.addWidget(name_frame)
        
        # Add stretch to push footer to bottom
        main_layout.addStretch()
        
        # Create footer
        footer = QFrame()
        footer.setStyleSheet("background-color: #2c3e50; padding: 15px;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 10, 20, 10)
        footer_label = QLabel("Created By Krish Devani SAMPLE GUI")
        footer_label.setStyleSheet("color: white; font-size: 14px;")
        footer_layout.addWidget(footer_label)
        main_layout.addWidget(footer)
        
        # Initialize nested dropdowns
        self.update_subcategory()
        self.update_city()
        self.update_team()
        
    def update_subcategory(self):
        self.subcategory_combo.clear()
        category = self.category_combo.currentText()
        if category == "Electronics":
            self.subcategory_combo.addItems(["Laptops", "Phones", "Tablets", "Accessories"])
        elif category == "Clothing":
            self.subcategory_combo.addItems(["Men", "Women", "Kids", "Accessories"])
        elif category == "Food":
            self.subcategory_combo.addItems(["Fruits", "Vegetables", "Dairy", "Bakery"])
        elif category == "Books":
            self.subcategory_combo.addItems(["Fiction", "Non-Fiction", "Educational", "Magazines"])
            
    def update_city(self):
        self.city_combo.clear()
        location = self.location_combo.currentText()
        if location == "North":
            self.city_combo.addItems(["New York", "Boston", "Chicago"])
        elif location == "South":
            self.city_combo.addItems(["Miami", "Houston", "Atlanta"])
        elif location == "East":
            self.city_combo.addItems(["Los Angeles", "San Francisco", "Seattle"])
        elif location == "West":
            self.city_combo.addItems(["Denver", "Phoenix", "Las Vegas"])
            
    def update_team(self):
        self.team_combo.clear()
        department = self.department_combo.currentText()
        if department == "IT":
            self.team_combo.addItems(["Development", "QA", "DevOps", "Support"])
        elif department == "HR":
            self.team_combo.addItems(["Recruitment", "Training", "Employee Relations"])
        elif department == "Finance":
            self.team_combo.addItems(["Accounting", "Tax", "Audit", "Investment"])
        elif department == "Marketing":
            self.team_combo.addItems(["Digital", "Content", "Brand", "Social Media"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SampleGUI()
    window.show()
    sys.exit(app.exec_()) 