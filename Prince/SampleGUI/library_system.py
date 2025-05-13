import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QTableWidget, QTableWidgetItem, QMessageBox, 
                            QTabWidget, QFormLayout, QComboBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from datetime import datetime

class Book:
    def __init__(self, title, author, isbn, status="Available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

class Borrower:
    def __init__(self, name, id_number, contact):
        self.name = name
        self.id_number = id_number
        self.contact = contact
        self.borrowed_books = []

class LibrarySystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 1000, 600)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #4a90e2;
                color: white;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #4a90e2;
                color: white;
                padding: 5px;
                border: none;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)
        
        # Initialize data storage
        self.books = []
        self.borrowers = []
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Create tabs
        self.create_books_tab(tabs)
        self.create_borrowers_tab(tabs)
        self.create_lending_tab(tabs)
        
        # Create footer
        footer = QFrame()
        footer.setFrameShape(QFrame.StyledPanel)
        footer.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
            }
        """)
        footer_layout = QHBoxLayout(footer)
        
        footer_label = QLabel("Made by Prince Diyora")
        footer_label.setStyleSheet("color: white; font-size: 12px;")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(footer_label)
        
        layout.addWidget(footer)
        
    def create_books_tab(self, tabs):
        books_widget = QWidget()
        layout = QVBoxLayout(books_widget)
        
        # Add book form
        form_layout = QFormLayout()
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Author:", self.author_input)
        form_layout.addRow("ISBN:", self.isbn_input)
        
        add_button = QPushButton("Add Book")
        add_button.clicked.connect(self.add_book)
        form_layout.addRow(add_button)
        
        layout.addLayout(form_layout)
        
        # Books table
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(4)
        self.books_table.setHorizontalHeaderLabels(["Title", "Author", "ISBN", "Status"])
        self.books_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.books_table)
        
        tabs.addTab(books_widget, "Books")
        
    def create_borrowers_tab(self, tabs):
        borrowers_widget = QWidget()
        layout = QVBoxLayout(borrowers_widget)
        
        # Add borrower form
        form_layout = QFormLayout()
        self.borrower_name_input = QLineEdit()
        self.borrower_id_input = QLineEdit()
        self.borrower_contact_input = QLineEdit()
        
        form_layout.addRow("Name:", self.borrower_name_input)
        form_layout.addRow("ID Number:", self.borrower_id_input)
        form_layout.addRow("Contact:", self.borrower_contact_input)
        
        add_button = QPushButton("Add Borrower")
        add_button.clicked.connect(self.add_borrower)
        form_layout.addRow(add_button)
        
        layout.addLayout(form_layout)
        
        # Borrowers table
        self.borrowers_table = QTableWidget()
        self.borrowers_table.setColumnCount(3)
        self.borrowers_table.setHorizontalHeaderLabels(["Name", "ID Number", "Contact"])
        self.borrowers_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.borrowers_table)
        
        tabs.addTab(borrowers_widget, "Borrowers")
        
    def create_lending_tab(self, tabs):
        lending_widget = QWidget()
        layout = QVBoxLayout(lending_widget)
        
        # Lending form
        form_layout = QFormLayout()
        self.borrower_combo = QComboBox()
        self.book_combo = QComboBox()
        
        form_layout.addRow("Borrower:", self.borrower_combo)
        form_layout.addRow("Book:", self.book_combo)
        
        lend_button = QPushButton("Lend Book")
        lend_button.clicked.connect(self.lend_book)
        form_layout.addRow(lend_button)
        
        return_button = QPushButton("Return Book")
        return_button.clicked.connect(self.return_book)
        form_layout.addRow(return_button)
        
        layout.addLayout(form_layout)
        
        # Lending history table
        self.lending_table = QTableWidget()
        self.lending_table.setColumnCount(4)
        self.lending_table.setHorizontalHeaderLabels(["Book", "Borrower", "Date", "Status"])
        self.lending_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.lending_table)
        
        tabs.addTab(lending_widget, "Lending")
        
    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        
        if not all([title, author, isbn]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
            
        book = Book(title, author, isbn)
        self.books.append(book)
        self.update_books_table()
        self.update_book_combo()
        
        # Clear inputs
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        
    def add_borrower(self):
        name = self.borrower_name_input.text()
        id_number = self.borrower_id_input.text()
        contact = self.borrower_contact_input.text()
        
        if not all([name, id_number, contact]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
            
        borrower = Borrower(name, id_number, contact)
        self.borrowers.append(borrower)
        self.update_borrowers_table()
        self.update_borrower_combo()
        
        # Clear inputs
        self.borrower_name_input.clear()
        self.borrower_id_input.clear()
        self.borrower_contact_input.clear()
        
    def update_books_table(self):
        self.books_table.setRowCount(len(self.books))
        for i, book in enumerate(self.books):
            self.books_table.setItem(i, 0, QTableWidgetItem(book.title))
            self.books_table.setItem(i, 1, QTableWidgetItem(book.author))
            self.books_table.setItem(i, 2, QTableWidgetItem(book.isbn))
            self.books_table.setItem(i, 3, QTableWidgetItem(book.status))
            
    def update_borrowers_table(self):
        self.borrowers_table.setRowCount(len(self.borrowers))
        for i, borrower in enumerate(self.borrowers):
            self.borrowers_table.setItem(i, 0, QTableWidgetItem(borrower.name))
            self.borrowers_table.setItem(i, 1, QTableWidgetItem(borrower.id_number))
            self.borrowers_table.setItem(i, 2, QTableWidgetItem(borrower.contact))
            
    def update_book_combo(self):
        self.book_combo.clear()
        for book in self.books:
            if book.status == "Available":
                self.book_combo.addItem(f"{book.title} ({book.isbn})", book)
                
    def update_borrower_combo(self):
        self.borrower_combo.clear()
        for borrower in self.borrowers:
            self.borrower_combo.addItem(f"{borrower.name} ({borrower.id_number})", borrower)
            
    def lend_book(self):
        if not self.book_combo.currentData() or not self.borrower_combo.currentData():
            QMessageBox.warning(self, "Error", "Please select both a book and a borrower")
            return
            
        book = self.book_combo.currentData()
        borrower = self.borrower_combo.currentData()
        
        book.status = "Borrowed"
        borrower.borrowed_books.append(book)
        
        # Update lending history
        row = self.lending_table.rowCount()
        self.lending_table.insertRow(row)
        self.lending_table.setItem(row, 0, QTableWidgetItem(book.title))
        self.lending_table.setItem(row, 1, QTableWidgetItem(borrower.name))
        self.lending_table.setItem(row, 2, QTableWidgetItem(datetime.now().strftime("%Y-%m-%d")))
        self.lending_table.setItem(row, 3, QTableWidgetItem("Borrowed"))
        
        self.update_books_table()
        self.update_book_combo()
        
    def return_book(self):
        # Implementation for returning books
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibrarySystem()
    window.show()
    sys.exit(app.exec_())