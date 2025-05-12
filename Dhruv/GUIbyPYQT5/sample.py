import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QLabel, 
    QDateEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QDate

class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal Expense Tracker")
        self.setGeometry(300, 200, 600, 500)

        # Layout for the input section
        self.layout = QVBoxLayout()

        # Header
        self.header = QLabel("Personal Expense Tracker")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            background-color: #4CAF50;
            padding: 10px;
        """)

        # Footer
        self.footer = QLabel("Expense Tracker App")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setStyleSheet("""
            font-size: 20px;
            color: white;
            background-color: #333333;
            padding: 5px;
        """)

        # Input for expense amount, category, and date
        self.input_layout = QHBoxLayout()
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Food", "Travel", "Bills", "Entertainment", "Others"])

        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())

        self.add_button = QPushButton("Add Expense")
        self.add_button.clicked.connect(self.add_expense)

        self.input_layout.addWidget(self.amount_input)
        self.input_layout.addWidget(self.category_combo)
        self.input_layout.addWidget(self.date_picker)
        self.input_layout.addWidget(self.add_button)

        # Table to display expenses
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Category", "Amount", "Delete"])
        self.table.setRowCount(0)

        # Total Expense Label
        self.total_label = QLabel("Total Expense: ₹0.00")
        self.layout.addWidget(self.header)
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.total_label)

        # Filter Layout
        self.filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Food", "Travel", "Bills", "Entertainment", "Others"])
        self.filter_combo.currentIndexChanged.connect(self.filter_expenses)
        self.filter_layout.addWidget(self.filter_combo)

        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.footer)

        self.setLayout(self.layout)

        # Expense list storage
        self.expenses = []

        # Styling for the app
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
                background-color: #fff3e0;
            }
            QLineEdit {
                padding: 4px;
                font-size: 14px;
            }
            QPushButton {
                padding: 6px;
                background-color: black;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                font-size: 20px;
                background-color: white;
                border: 1px solid #ddd;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QComboBox {
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
        """)

    def add_expense(self):
        # Get input data
        amount = self.amount_input.text().strip()
        category = self.category_combo.currentText()
        date = self.date_picker.date().toString("dd/MM/yyyy")

        if not amount.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount!")
            return

        # Add expense to the list
        self.expenses.append({"amount": float(amount), "category": category, "date": date})

        # Update the table
        self.update_table()

        # Clear input fields
        self.amount_input.clear()

    def update_table(self):
        # Clear the table
        self.table.setRowCount(0)

        # Add expenses to the table
        total = 0
        for row, expense in enumerate(self.expenses):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(expense["date"]))
            self.table.setItem(row, 1, QTableWidgetItem(expense["category"]))
            self.table.setItem(row, 2, QTableWidgetItem(f"₹{expense['amount']:.2f}"))

            # Add Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, r=row: self.delete_expense(r))
            self.table.setCellWidget(row, 3, delete_button)

            total += expense["amount"]

        self.total_label.setText(f"Total Expense: ₹{total:.2f}")

    def delete_expense(self, row):
        # Remove expense from the list
        del self.expenses[row]
        self.update_table()

    def filter_expenses(self):
        filter_category = self.filter_combo.currentText()

        # Filter the expenses by category
        filtered_expenses = []
        if filter_category == "All":
            filtered_expenses = self.expenses
        else:
            for expense in self.expenses:
                if expense["category"] == filter_category:
                    filtered_expenses.append(expense)

        # Update the table with filtered data
        self.expenses = filtered_expenses
        self.update_table()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec_())
