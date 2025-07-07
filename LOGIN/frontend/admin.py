from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                            QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
                            QComboBox, QDialog, QLineEdit, QTabWidget, QInputDialog)
from PyQt5.QtCore import Qt
import requests
import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from projectmanager_welcome import ProjectManagerWelcome
from user_welcome import ManagerWelcome
from employee_welcome import EmployeeWelcome

class AdminDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel('Admin Dashboard')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Regular Users Tab
        users_tab = QWidget()
        users_layout = QVBoxLayout()
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(2)
        self.users_table.setHorizontalHeaderLabels(['Username', 'Delete'])
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        users_layout.addWidget(self.users_table)
        
        users_tab.setLayout(users_layout)

        # Company Personnel Tab
        company_tab = QWidget()
        company_layout = QVBoxLayout()
        
        # Add user button
        add_button = QPushButton('Add New User')
        add_button.clicked.connect(self.add_user)
        company_layout.addWidget(add_button)
        
        # Company personnel table
        self.company_table = QTableWidget()
        self.company_table.setColumnCount(4)
        self.company_table.setHorizontalHeaderLabels(['Username', 'Role', 'Delete', 'Access'])
        self.company_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        company_layout.addWidget(self.company_table)
        
        company_tab.setLayout(company_layout)

        # Add tabs to tab widget
        self.tab_widget.addTab(users_tab, "Regular Users")
        self.tab_widget.addTab(company_tab, "Company Personnel")
        
        layout.addWidget(self.tab_widget)

        # Logout button
        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(self.main_window.logout)
        layout.addWidget(logout_button)

        self.setLayout(layout)
        self.load_users()

    def load_users(self):
        try:
            response = requests.get('http://localhost:8000/api/users/')
            if response.status_code == 200:
                users = response.json()
                
                # Filter users for each table
                regular_users = [u for u in users if u['role'] == 'user']
                company_users = [u for u in users if u['role'] != 'user']
                
                # Update regular users table
                self.users_table.setRowCount(len(regular_users))
                for row, user in enumerate(regular_users):
                    # Username
                    username_item = QTableWidgetItem(user['username'])
                    username_item.setFlags(username_item.flags() & ~Qt.ItemIsEditable)
                    self.users_table.setItem(row, 0, username_item)
                    
                    # Delete button
                    delete_btn = QPushButton('Delete')
                    delete_btn.clicked.connect(lambda checked, u=user['username']: self.delete_user(u))
                    self.users_table.setCellWidget(row, 1, delete_btn)
                
                # Update company personnel table
                self.company_table.setRowCount(len(company_users))
                for row, user in enumerate(company_users):
                    # Username
                    username_item = QTableWidgetItem(user['username'])
                    username_item.setFlags(username_item.flags() & ~Qt.ItemIsEditable)
                    self.company_table.setItem(row, 0, username_item)
                    
                    # Role
                    role_item = QTableWidgetItem(user['role'])
                    role_item.setFlags(role_item.flags() & ~Qt.ItemIsEditable)
                    self.company_table.setItem(row, 1, role_item)
                    
                    # Delete button
                    delete_btn = QPushButton('Delete')
                    delete_btn.clicked.connect(lambda checked, u=user['username']: self.delete_user(u))
                    self.company_table.setCellWidget(row, 2, delete_btn)

                    # Access button
                    access_btn = QPushButton('Access')
                    access_btn.clicked.connect(lambda checked, u=user['username'], r=user['role']: self.access_user_window(u, r))
                    self.company_table.setCellWidget(row, 3, access_btn)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load users: {str(e)}')

    def delete_user(self, username):
        # Show dialog to get delete reason
        reason, ok = QInputDialog.getText(self, 'Delete User', 
                                        'Please provide a reason for deletion:',
                                        QLineEdit.Normal)
        if ok and reason:
            try:
                response = requests.delete(
                    f'http://localhost:8000/api/users/{username}/',
                    json={'reason': reason, 'deleted_by': 'admin'}
                )
                if response.status_code == 200:
                    QMessageBox.information(self, 'Success', 'User deleted successfully')
                    self.load_users()  # Refresh the tables
                else:
                    QMessageBox.warning(self, 'Error', response.json().get('error', 'Failed to delete user'))
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete user: {str(e)}')
        elif ok:  # User clicked OK but didn't provide a reason
            QMessageBox.warning(self, 'Error', 'Please provide a reason for deletion')

    def add_user(self):
        dialog = AddUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()  # Refresh the tables

    def access_user_window(self, username, role):
        if role == 'project manager':
            window = ProjectManagerWelcome(username, self)
        elif role == 'user':
            window = ManagerWelcome(username, self)
        else:  # employee
            window = EmployeeWelcome(username, self)
        
        window.show()

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add New User')
        layout = QVBoxLayout()

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Role selection
        self.role_combo = QComboBox()
        self.role_combo.addItems(['project manager', 'employee'])  # Only company roles
        layout.addWidget(self.role_combo)

        # Buttons
        button_layout = QHBoxLayout()
        
        add_button = QPushButton('Add')
        add_button.clicked.connect(self.accept)
        button_layout.addWidget(add_button)
        
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def accept(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()

        if not all([username, password]):
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        try:
            response = requests.post('http://localhost:8000/api/signup/',
                                  json={'username': username, 'password': password, 'role': role})
            
            if response.status_code in [200, 201]:
                QMessageBox.information(self, 'Success', 'User added successfully')
                super().accept()
            else:
                QMessageBox.warning(self, 'Error', response.json().get('error', 'Failed to add user'))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add user: {str(e)}') 