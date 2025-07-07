import sys
import os
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
    QLineEdit, QFormLayout, QInputDialog
)
from PyQt5.QtCore import Qt

API_BASE_URL = "http://127.0.0.1:8000"
STAGES = ["Material", "Manufacturing", "Packaging", "Dispatch", "Completed"]

# Place the QSS string at the top for reuse
QSS_GLOBAL = '''
QWidget {
    font-family: 'Segoe UI', Segoe UI, Arial, sans-serif;
    font-size: 11pt;
    background-color: #ffffff;
    color: #333333;
}

QPushButton {
    padding: 10px;
    border-radius: 5px;
    background-color: #007bff;
    color: white;
    border: none;
}
QPushButton:hover {
    background-color: #0056b3;
}
QPushButton:pressed {
    background-color: #004085;
}
QPushButton[stage="true"] {
    background-color: #28a745;
}
QPushButton[stage="true"]:disabled {
    background-color: #94d3a2;
    color: #ccc;
}
QPushButton[stage="true"]:hover:!disabled {
    background-color: #218838;
}

QTableWidget {
    border: 1px solid #ccc;
    background-color: #fff;
    gridline-color: #dee2e6;
}
QHeaderView::section {
    background-color: #f8f9fa;
    padding: 6px;
    border: none;
    font-weight: bold;
    color: #333;
}
QLineEdit, QSpinBox, QTextEdit {
    padding: 8px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    background-color: #ffffff;
}
QLineEdit:focus, QSpinBox:focus, QTextEdit:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
QLabel#statusLabel {
    color: gray;
}
QLabel#errorLabel {
    color: red;
}
'''

def show_error(message):
    QMessageBox.critical(None, "Error", message)

class StageSelectionWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.setStyleSheet(QSS_GLOBAL)
        self.main_window = main_window
        self.setWindowTitle("Select Stage")
        self.resize(300, 250)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select your stage:"))

        for stage in STAGES[:-1]:  # Exclude "Completed" for interaction
            btn = QPushButton(stage)
            btn.clicked.connect(lambda _, s=stage: self.open_login_window(s))
            layout.addWidget(btn)

        # Add the View Completed Items button
        completed_btn = QPushButton("View Completed Items")
        completed_btn.clicked.connect(self.open_completed_window)
        layout.addWidget(completed_btn)

        # Add Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def logout(self):
        self.close()
        if self.main_window:
            self.main_window.show()

    def open_login_window(self, stage_name):
        self.hide()
        self.login_window = LoginWindow(stage_name, self)
        self.login_window.show()

    def open_completed_window(self):
        self.hide()
        self.completed_window = CompletedStageWindow(self)
        self.completed_window.show()

class LoginWindow(QWidget):
    def __init__(self, stage_name, stage_selector):
        super().__init__()
        self.setStyleSheet(QSS_GLOBAL)
        self.stage_name = stage_name
        self.stage_selector = stage_selector
        self.setWindowTitle(f"{stage_name} - Login")
        self.resize(300, 150)

        layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addRow("Username:", self.username_input)
        self.form_layout.addRow("Password:", self.password_input)

        layout.addLayout(self.form_layout)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.hide()
            self.stage_window = StageWindow(self.stage_name, self.stage_selector)
            self.stage_window.show()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")

class StageWindow(QWidget):
    def __init__(self, stage_name, stage_selector):
        super().__init__()
        self.setStyleSheet(QSS_GLOBAL)
        self.stage_name = stage_name
        self.stage_selector = stage_selector
        self.setWindowTitle(f"{stage_name} Stage Dashboard")
        self.resize(800, 500)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Order ID", "Customer", "Item", "Quantity", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(QLabel(f"Current Stage: {stage_name}"))
        layout.addWidget(self.table)

        self.load_button = QPushButton("Refresh Orders")
        self.load_button.clicked.connect(self.load_orders)
        layout.addWidget(self.load_button)

        # Add Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)
        self.load_orders()

    def logout(self):
        self.close()
        self.stage_selector.show()

    def closeEvent(self, event):
        # Show stage selector again on close
        self.stage_selector.show()
        event.accept()

    def load_orders(self):
        self.table.setRowCount(0)
        try:
            response = requests.get(f"{API_BASE_URL}/api/get-orders/?status={self.stage_name}")
            if response.status_code == 200:
                text = response.text.strip()
                if not text:
                    show_error("No data received from server.")
                    return

                orders = json.loads(text)
                if not isinstance(orders, list):
                    show_error("Invalid data format received.")
                    return

                for order in orders:
                    # Add each item from the order to the table
                    for item in order.get("items", []):
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        self.table.setItem(row, 0, QTableWidgetItem(order.get("order_id", "")))
                        self.table.setItem(row, 1, QTableWidgetItem(order.get("customer", {}).get("name", "Unknown")))
                        self.table.setItem(row, 2, QTableWidgetItem(item.get("name", "")))
                        self.table.setItem(row, 3, QTableWidgetItem(str(item.get("quantity", 0))))

                        # Create button with item data
                        btn = QPushButton("Next Stage")
                        # Store the item data in the button's properties
                        btn.setProperty("item_id", str(item.get("id")))  # Store as string
                        btn.clicked.connect(lambda checked, b=btn: self.update_stage(b))
                        self.table.setCellWidget(row, 4, btn)
            else:
                show_error(f"HTTP Error {response.status_code}")
        except Exception as e:
            show_error(f"Failed to load orders:\n{str(e)}")

    def update_stage(self, button):
        """Updates an item's stage and sends an email to the next stage handler."""
        # Get item ID from button property
        item_id = button.property("item_id")
        if not item_id:
            show_error("Item ID not found")
            return

        try:
            # Convert item ID to integer
            item_id = int(item_id)
        except ValueError:
            show_error("Invalid item ID format")
            return

        current_index = STAGES.index(self.stage_name)
        if current_index + 1 >= len(STAGES):
            QMessageBox.information(self, "Done", "Item is already in the final stage.")
            return

        next_stage = STAGES[current_index + 1]
        notes, ok = QInputDialog.getText(self, "Notes", f"Enter notes for moving to {next_stage}:")
        if not ok:
            return

        try:
            # Print the data being sent for debugging
            data = {
                "item_id": item_id,
                "next_stage": next_stage,
                "notes": notes
            }
            print(f"Sending data to backend: {data}")  # Debug print

            res = requests.post(f"{API_BASE_URL}/api/update_item/", json=data)
            if res.status_code == 200:
                QMessageBox.information(self, "Updated", "Stage updated and email sent.")
                # Automatically open the next stage window and close this one
                self.close()
                self.next_stage_window = StageWindow(next_stage, self.stage_selector)
                self.next_stage_window.show()
            else:
                QMessageBox.warning(self, "Failed", f"Server error: {res.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update stage:\n{str(e)}")

class CompletedStageWindow(QWidget):
    def __init__(self, stage_selector):
        super().__init__()
        self.setStyleSheet(QSS_GLOBAL)
        self.stage_selector = stage_selector
        self.setWindowTitle("Completed Items")
        self.resize(800, 500)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Order ID", "Customer", "Item", "Quantity", "Completed At"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(QLabel("Completed Items"))
        layout.addWidget(self.table)

        self.load_button = QPushButton("Refresh Completed Items")
        self.load_button.clicked.connect(self.load_completed_items)
        layout.addWidget(self.load_button)

        # Add Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)
        self.load_completed_items()

    def logout(self):
        self.close()
        self.stage_selector.show()

    def closeEvent(self, event):
        # Show stage selector again on close
        self.stage_selector.show()
        event.accept()

    def load_completed_items(self):
        self.table.setRowCount(0)
        try:
            response = requests.get(f"{API_BASE_URL}/api/get-orders/?status=Completed")
            if response.status_code == 200:
                text = response.text.strip()
                if not text:
                    show_error("No data received from server.")
                    return

                orders = json.loads(text)
                if not isinstance(orders, list):
                    show_error("Invalid data format received.")
                    return

                for order in orders:
                    for item in order.get("items", []):
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        self.table.setItem(row, 0, QTableWidgetItem(order.get("order_id", "")))
                        self.table.setItem(row, 1, QTableWidgetItem(order.get("customer", {}).get("name", "Unknown")))
                        self.table.setItem(row, 2, QTableWidgetItem(item.get("name", "")))
                        self.table.setItem(row, 3, QTableWidgetItem(str(item.get("quantity", 0))))
                        # Find completion time from status_history if available
                        completed_at = ""
                        for h in order.get("status_history", []):
                            if h.get("status") == "Completed":
                                completed_at = h.get("created_at", "")
                        self.table.setItem(row, 4, QTableWidgetItem(completed_at))
            else:
                show_error(f"HTTP Error {response.status_code}")
        except Exception as e:
            show_error(f"Failed to load completed items:\n{str(e)}")

# Add a simple main login window for demonstration
class MainLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 150)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome! Please log in."))
        self.setLayout(layout)

if __name__ == "__main__":
    QApplication.setStyle("Fusion")
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS_GLOBAL)
    stage_selector = StageSelectionWindow()
    stage_selector.show()
    sys.exit(app.exec_())
