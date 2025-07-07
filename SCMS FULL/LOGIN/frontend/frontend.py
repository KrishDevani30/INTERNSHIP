from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QLineEdit, QMessageBox,
                            QComboBox, QStackedWidget, QRadioButton, QButtonGroup,
                            QTabWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import requests
import importlib.util
import sys
import os

# Add the project root to the Python path to resolve module import errors
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# --- Dummy Classes for Demonstration ---
# These are placeholder widgets to make the application runnable.
# Replace them with your actual application widgets.
try:
    from SHOP.scms_frontend import SCMSApp
except ImportError:
    class SCMSApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Shop")
            self.setCentralWidget(QLabel("Shopping App"))
        def set_current_user(self, username):
            self.setWindowTitle(f"Shop - {username}")

try:
    from PRODUCTMANAGER.product_manager_gui import ProductManagerGUI
except ImportError:
    class ProductManagerGUI(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Product Manager")
            self.setCentralWidget(QLabel("Product Manager GUI"))

try:
    from SUPPLYCHAIN.frontend.employee import StageSelectionWindow
except ImportError:
    class StageSelectionWindow(QMainWindow):
        def __init__(self, main_window=None):
            super().__init__()
            self.main_window = main_window
            self.setWindowTitle("Employee Task")
            self.setCentralWidget(QLabel("Stage Selection"))

class ProjectManagerWelcome(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Project Manager")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Welcome Project Manager {username}"))
        self.resize(400, 300)

class ManagerWelcome(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manager")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Welcome Manager {username}"))
        self.resize(400, 300)
        
class EmployeeWelcome(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Employee")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Welcome Employee {username}"))
        self.resize(400, 300)

from LOGIN.frontend.admin import AdminDashboard

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from projectmanager_welcome import ProjectManagerWelcome
from user_welcome import ManagerWelcome
from employee_welcome import EmployeeWelcome
from admin import AdminDashboard

# Modern Blue QSS Theme
GLOBAL_STYLE = """
#mainWidget {
    border-radius: 20px;
}

#leftPanel {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0052D4, stop:1 #4364F7);
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
}
#leftPanel QLabel {
    background-color: transparent;
    color: white;
}
#welcomeLabel {
    font-size: 24px;
    font-weight: 300;
}
#spacerLabel {
    font-size: 48px;
    font-weight: bold;
}
#descriptionLabel {
    font-size: 14px;
    font-weight: 300;
}

#rightPanel {
    background-color: white;
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
}
#rightPanel #titleLabel {
    color: #2c3e50;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
}
#rightPanel QLineEdit {
    border: none;
    border-bottom: 1px solid #bdc3c7;
    background-color: transparent;
    padding: 10px 5px;
    font-size: 15px;
    color: #2c3e50;
    margin-bottom: 15px;
}
#rightPanel QLineEdit:focus {
    border-bottom: 2px solid #3498db;
}
#rightPanel QPushButton {
    background-color: #3498db;
    color: white;
    font-weight: bold;
    font-size: 14px;
    padding: 12px 20px;
    border: none;
    border-radius: 18px;
    margin-top: 10px;
}
#rightPanel QPushButton:hover {
    background-color: #2980b9;
}
#rightPanel #switchButton {
    background-color: transparent;
    color: #3498db;
    font-weight: normal;
    font-size: 12px;
    text-decoration: none;
    border: 1px solid #3498db;
}
#rightPanel #switchButton:hover {
    background-color: #3498db;
    color: white;
}
#rightPanel QTabBar::tab {
    background: transparent;
    color: #7f8c8d;
    font-weight: bold;
    font-size: 15px;
    padding: 10px 15px;
    border: none;
    border-bottom: 2px solid #ecf0f1;
    margin-right: 10px;
    min-width: 90px;
    text-align: center;
}
#rightPanel QTabBar::tab:selected {
    color: #3498db;
    border-bottom: 2px solid #3498db;
}
#rightPanel QTabBar::tab:hover {
    color: #2980b9;
    border-bottom: 2px solid #aed6f1;
}
#rightPanel QTabWidget::pane {
    border: none;
}
#rightPanel QTabWidget {
    margin-top: 15px;
} 
"""

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Panel
        left_panel = QWidget()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)
        
        welcome_label = QLabel("Welcome to")
        welcome_label.setObjectName("welcomeLabel")
        spacer_label = QLabel("SCMS App")
        spacer_label.setObjectName("spacerLabel")
        description_label = QLabel("A powerful solution to simplify, automate, and optimize every step of your supply chain — from procurement to delivery.")
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)

        left_layout.addStretch(1)
        left_layout.addWidget(welcome_label, 0, Qt.AlignCenter)
        left_layout.addWidget(spacer_label, 0, Qt.AlignCenter)
        left_layout.addStretch(1)
        left_layout.addWidget(description_label, 0, Qt.AlignCenter)
        left_layout.addStretch(2)

        # Right Panel
        right_panel = QWidget()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        title_label = QLabel('Login')
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title_label, 0, Qt.AlignTop)

        self.tab_widget = QTabWidget()
        
        user_tab = QWidget()
        user_layout = QVBoxLayout(user_tab)
        user_layout.setContentsMargins(0, 20, 0, 0)
        self.user_username_input = QLineEdit(placeholderText='Username')
        self.user_password_input = QLineEdit(placeholderText='Password', echoMode=QLineEdit.Password)
        user_login_button = QPushButton('Login')
        user_login_button.clicked.connect(lambda: self.login('user'))
        user_layout.addWidget(self.user_username_input)
        user_layout.addWidget(self.user_password_input)
        user_layout.addWidget(user_login_button)
        
        switch_to_signup = QPushButton("Don't have an account? Sign Up")
        switch_to_signup.setObjectName("switchButton")
        switch_to_signup.clicked.connect(lambda: self.main_window.stacked_widget.setCurrentIndex(1))
        user_layout.addWidget(switch_to_signup)
        user_layout.addStretch()

        company_tab = QWidget()
        company_layout = QVBoxLayout(company_tab)
        company_layout.setContentsMargins(0, 20, 0, 0)
        self.company_username_input = QLineEdit(placeholderText='Username')
        self.company_password_input = QLineEdit(placeholderText='Password', echoMode=QLineEdit.Password)
        company_login_button = QPushButton('Login')
        company_login_button.clicked.connect(lambda: self.login('company'))
        company_layout.addWidget(self.company_username_input)
        company_layout.addWidget(self.company_password_input)
        company_layout.addWidget(company_login_button)
        company_layout.addStretch()

        self.tab_widget.addTab(user_tab, "User")
        self.tab_widget.addTab(company_tab, "Company")
        
        right_layout.addWidget(self.tab_widget)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)

    def clear_fields(self):
        self.user_username_input.clear()
        self.user_password_input.clear()
        self.company_username_input.clear()
        self.company_password_input.clear()

    def login(self, login_type):
        if login_type == 'user':
            username = self.user_username_input.text()
            password = self.user_password_input.text()
        else:
            username = self.company_username_input.text()
            password = self.company_password_input.text()

        if not username or not password:
            print('DEBUG: Empty fields error')
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        try:
            response = requests.post('http://localhost:8000/api/login/', json={
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                data = response.json()
                # If company login and admin, show admin dashboard
                if login_type == 'company' and username == 'admin' and data['role'] == 'admin':
                    self.main_window.show_welcome_page('admin', username)
                    self.clear_fields()
                    return
                # For company login, only allow admin, project manager, and employee roles
                if login_type == 'company' and data['role'] not in ['admin', 'project manager', 'employee']:
                    print('DEBUG: Invalid company login type')
                    QMessageBox.warning(self, 'Error', 'Invalid login type for company access')
                    return
                # For user login, only allow user role
                if login_type == 'user' and data['role'] != 'user':
                    print('DEBUG: Invalid user login type')
                    QMessageBox.warning(self, 'Error', 'Invalid login type for user access')
                    return
                
                self.main_window.show_welcome_page(data['role'], username)
                self.clear_fields()
            else:
                try:
                    error_msg = response.json().get('error', 'Login failed')
                except Exception:
                    error_msg = response.text or 'Login failed'
                print('DEBUG: Error message from backend:', repr(error_msg))
                QMessageBox.warning(self, 'Error', str(error_msg))
        except Exception as e:
            print('DEBUG: Exception in login:', str(e))
            QMessageBox.critical(self, 'Error', f'Failed to login: {str(e)}')

class SignupWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Panel (similar to login)
        left_panel = QWidget()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)
        welcome_label = QLabel("Create Account")
        welcome_label.setObjectName("welcomeLabel")
        spacer_label = QLabel("SCMS App")
        spacer_label.setObjectName("spacerLabel")
        description_label = QLabel("Join us and start managing your projects efficiently.")
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        left_layout.addStretch(1)
        left_layout.addWidget(welcome_label, 0, Qt.AlignCenter)
        left_layout.addWidget(spacer_label, 0, Qt.AlignCenter)
        left_layout.addStretch(1)
        left_layout.addWidget(description_label, 0, Qt.AlignCenter)
        left_layout.addStretch(2)

        # Right Panel
        right_panel = QWidget()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        title_label = QLabel('Sign Up')
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 20, 0, 0)
        self.username_input = QLineEdit(placeholderText='Username')
        self.password_input = QLineEdit(placeholderText='Password', echoMode=QLineEdit.Password)
        self.confirm_password_input = QLineEdit(placeholderText='Confirm Password', echoMode=QLineEdit.Password)
        signup_button = QPushButton('Sign Up')
        signup_button.clicked.connect(self.signup)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addWidget(signup_button)
        
        back_button = QPushButton('Already have an account? Login')
        back_button.setObjectName("switchButton")
        back_button.clicked.connect(lambda: self.main_window.stacked_widget.setCurrentIndex(0))
        form_layout.addWidget(back_button)
        form_layout.addStretch()

        right_layout.addWidget(title_label, 0, Qt.AlignTop)
        right_layout.addWidget(form_widget)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()

    def signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            print('DEBUG: Empty fields error (signup)')
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        if password != confirm_password:
            print('DEBUG: Passwords do not match')
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return

        try:
            response = requests.post('http://localhost:8000/api/signup/', json={
                'username': username,
                'password': password,
                'role': 'user'
            })
            
            if response.status_code in [200, 201]:
                QMessageBox.information(self, 'Success', 'Signup successful! Please login.')
                self.clear_fields()
                self.main_window.stacked_widget.setCurrentIndex(0)
            else:
                try:
                    error_msg = response.json().get('error', 'Signup failed')
                except Exception:
                    error_msg = response.text or 'Signup failed'
                print('DEBUG: Error message from backend (signup):', repr(error_msg))
                QMessageBox.warning(self, 'Error', str(error_msg))
        except Exception as e:
            print('DEBUG: Exception in signup:', str(e))
            QMessageBox.critical(self, 'Error', f'Failed to signup: {str(e)}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.windows = {}
        self.mouse_pressed = False
        self.old_pos = None

    def initUI(self):
        self.setWindowTitle('Spacer App')
        self.setGeometry(100, 100, 900, 550)
        # Add QMessageBox QSS to ensure error dialogs are readable
        self.setStyleSheet(GLOBAL_STYLE + """
QMessageBox {
    background: white;
    color: black;
}
QMessageBox QLabel {
    color: black;
    font-size: 14px;
}
QMessageBox QPushButton {
    color: black;
    background: #e0e0e0;
    border-radius: 8px;
    padding: 6px 16px;
}
""")

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("mainWidget")
        
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0,0,0,0)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.login_page = LoginWindow(self)
        self.signup_page = SignupWindow(self)
        
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def show_welcome_page(self, role, username):
        if role == 'admin':
            # For admin, add the dashboard to the same window and switch to it
            self.admin_dashboard_page = AdminDashboard(self)
            self.stacked_widget.addWidget(self.admin_dashboard_page)
            self.stacked_widget.setCurrentWidget(self.admin_dashboard_page)
            return
        # For other roles, hide the login window and open a new one
        self.hide()
        
        win = None
        if role == 'user':
            # Dynamically import SCMSApp from SHOP/scms_frontend.py
            shop_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../SHOP/scms_frontend.py'))
            spec = importlib.util.spec_from_file_location('scms_frontend', shop_path)
            shop_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(shop_module)
            SCMSApp = shop_module.SCMSApp
            # Change working directory to SHOP directory so images and CSS are found
            os.chdir(os.path.dirname(shop_path))
            win = SCMSApp()
            win.set_current_user(username)
        elif role == 'project manager':
            # Dynamically import ProductManagerGUI from PRODUCTMANAGER/product_manager_gui.py
            pm_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../PRODUCTMANAGER/product_manager_gui.py'))
            spec = importlib.util.spec_from_file_location('product_manager_gui', pm_path)
            pm_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(pm_module)
            ProductManagerGUI = pm_module.ProductManagerGUI
            # Change working directory to PRODUCTMANAGER directory
            os.chdir(os.path.dirname(pm_path))
            win = ProductManagerGUI()
        elif role == 'employee':
            # Dynamically import StageSelectionWindow from SUPPLYCHAIN/frontend/employee.py
            employee_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../SUPPLYCHAIN/frontend/employee.py'))
            spec = importlib.util.spec_from_file_location('employee', employee_path)
            employee_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(employee_module)
            StageSelectionWindow = employee_module.StageSelectionWindow
            # Change working directory to SUPPLYCHAIN/frontend directory
            os.chdir(os.path.dirname(employee_path))
            win = StageSelectionWindow(main_window=self)
        else:
            win = EmployeeWelcome(username, self)
        
        if win:
            self.windows[role] = win
            win.show()

    def logout(self):
        # Close any external windows if they exist
        for window in self.windows.values():
            window.close()
        self.windows.clear()

        # If the admin dashboard is active, remove it
        if hasattr(self, 'admin_dashboard_page'):
            self.stacked_widget.removeWidget(self.admin_dashboard_page)
            del self.admin_dashboard_page

        # Show the main window again if it was hidden
        self.show()
        # Switch back to the login page
        self.stacked_widget.setCurrentIndex(0)
        # Clear the login form
        self.login_page.clear_fields()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed and self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False
        self.old_pos = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 