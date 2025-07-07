from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class ProjectManagerWelcome(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.username = username
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Welcome message
        welcome_label = QLabel(f'Welcome {self.username}!')
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Role message
        role_label = QLabel('You are logged in as Project Manager')
        role_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(role_label)
        
        # Additional message
        message_label = QLabel('You have project management and administrative privileges')
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label)
        
        # Logout button
        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(self.main_window.logout)
        layout.addWidget(logout_button)
        
        self.setLayout(layout) 