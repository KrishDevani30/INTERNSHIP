# Library Management System

A modern and user-friendly library management system built with PyQt5 that helps manage books, borrowers, and lending operations.

## Features

### 1. Book Management
- Add new books with details:
  - Title
  - Author
  - ISBN
  - Status (Available/Borrowed)
- View all books in a table format
- Track book availability status

### 2. Borrower Management
- Add new borrowers with details:
  - Name
  - ID Number
  - Contact Information
- View all registered borrowers
- Track borrowed books per borrower

### 3. Lending System
- Lend books to registered borrowers
- Track lending history with:
  - Book details
  - Borrower information
  - Lending date
  - Status
- Return book functionality

## Code Structure and Functions

### Class: Book
```python
class Book:
    def __init__(self, title, author, isbn, status="Available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status
```
- Stores book information including title, author, ISBN, and availability status
- Default status is set to "Available"

### Class: Borrower
```python
class Borrower:
    def __init__(self, name, id_number, contact):
        self.name = name
        self.id_number = id_number
        self.contact = contact
        self.borrowed_books = []
```
- Manages borrower information and their borrowed books
- Tracks borrower's personal details and maintains a list of borrowed books

### Class: LibrarySystem
Main application class that handles the GUI and all operations.

#### Initialization Functions
- `__init__()`: Sets up the main window, styling, and initializes data structures
- `create_books_tab()`: Creates the books management interface
- `create_borrowers_tab()`: Creates the borrowers management interface
- `create_lending_tab()`: Creates the lending operations interface

#### Book Management Functions
- `add_book()`: 
  - Validates and adds new books to the system
  - Updates the books table and combo box
  - Clears input fields after successful addition

- `update_books_table()`:
  - Refreshes the books table with current data
  - Displays all books with their current status

#### Borrower Management Functions
- `add_borrower()`:
  - Validates and adds new borrowers
  - Updates the borrowers table and combo box
  - Clears input fields after successful addition

- `update_borrowers_table()`:
  - Refreshes the borrowers table with current data
  - Displays all registered borrowers

#### Lending System Functions
- `update_book_combo()`:
  - Updates the book selection dropdown
  - Only shows available books

- `update_borrower_combo()`:
  - Updates the borrower selection dropdown
  - Shows all registered borrowers

- `lend_book()`:
  - Handles book lending process
  - Updates book status to "Borrowed"
  - Records lending history
  - Updates relevant tables and dropdowns

- `return_book()`:
  - Handles book return process
  - Updates book status back to "Available"
  - Updates lending history

## Technical Details

### Requirements
- Python 3.x
- PyQt5

### Installation
1. Install Python 3.x from [python.org](https://python.org)
2. Install PyQt5 using pip:
```bash
pip install PyQt5
```

### Running the Application
```bash
python library_system.py
```

## User Interface

### Books Tab
- Form to add new books
- Table displaying all books with their details
- Status tracking for each book

### Borrowers Tab
- Form to register new borrowers
- Table showing all registered borrowers
- Contact information management

### Lending Tab
- Dropdown menus to select books and borrowers
- Lend and Return book buttons
- Lending history table


## Author
Made by Prince Diyora 