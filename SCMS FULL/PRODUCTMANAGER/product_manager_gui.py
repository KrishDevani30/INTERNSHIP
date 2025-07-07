import sys
import os
import base64
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                            QPushButton, QFileDialog, QScrollArea, QFrame,
                            QGridLayout, QMessageBox, QComboBox, QSpinBox,
                            QDoubleSpinBox, QFormLayout, QSizePolicy)
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QBuffer, QByteArray
import sqlite3
from datetime import datetime
import importlib
import json

class StyledButton(QPushButton):
    def __init__(self, text, primary=False):
        super().__init__(text)
        self.setMinimumHeight(40)
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #E0E0E0;
                    color: #424242;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #BDBDBD;
                }
                QPushButton:pressed {
                    background-color: #9E9E9E;
                }
            """)

class ProductManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDatabase()
        self.loadProducts()
        self.setAcceptDrops(True)  # Enable drag and drop

    def initUI(self):
        self.setWindowTitle('Product Manager')
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QLabel {
                color: #424242;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #2196F3;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Left panel for adding products
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.StyledPanel)
        left_panel.setMaximumWidth(500)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(20, 20, 20, 20)

        # Header with logout button
        header_layout = QHBoxLayout()
        header_label = QLabel('Add New Product')
        header_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1976D2;
                padding-bottom: 10px;
            }
        """)
        header_layout.addWidget(header_label)
        
        # Add logout button
        logout_button = StyledButton('Logout')
        logout_button.clicked.connect(self.logout)
        header_layout.addWidget(logout_button)
        
        left_layout.addLayout(header_layout)
        
        # Add separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #E0E0E0;")
        left_layout.addWidget(separator)

        # Form elements
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Basic Information
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Product Name')
        self.name_input.setMinimumHeight(35)
        form_layout.addRow('Product Name:', self.name_input)

        self.product_id = QLineEdit()
        self.product_id.setPlaceholderText('e.g., PRD-001')
        self.product_id.setMinimumHeight(35)
        form_layout.addRow('Product ID:', self.product_id)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText('Product Description')
        self.description_input.setMaximumHeight(80)
        form_layout.addRow('Description:', self.description_input)

        # Category and Supplier
        self.category_combo = QComboBox()
        self.category_combo.addItems(['Electronics', 'Mechanical', 'Electrical', 'Software', 'Other'])
        self.category_combo.setMinimumHeight(35)
        form_layout.addRow('Category:', self.category_combo)

        self.supplier_input = QLineEdit()
        self.supplier_input.setPlaceholderText('Supplier Name')
        self.supplier_input.setMinimumHeight(35)
        form_layout.addRow('Supplier:', self.supplier_input)

        # Quantity and Cost
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 10000)
        self.quantity_spin.setValue(0)
        self.quantity_spin.setMinimumHeight(35)
        form_layout.addRow('Quantity:', self.quantity_spin)

        self.cost_spin = QDoubleSpinBox()
        self.cost_spin.setRange(0.00, 1000000.00)
        self.cost_spin.setDecimals(2)
        self.cost_spin.setPrefix('$ ')
        self.cost_spin.setMinimumHeight(35)
        form_layout.addRow('Cost:', self.cost_spin)

        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(['In Stock', 'Low Stock', 'Out of Stock', 'Discontinued'])
        self.status_combo.setMinimumHeight(35)
        form_layout.addRow('Status:', self.status_combo)

        # Image selection
        self.image_label = QLabel('Drag and drop an image here\nor click to select')
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #BDBDBD;
                border-radius: 8px;
                background-color: #FAFAFA;
                color: #757575;
            }
            QLabel:hover {
                border: 2px dashed #2196F3;
                background-color: #F5F5F5;
            }
        """)
        self.image_label.mousePressEvent = self.selectImage  # Make label clickable

        self.image_path = None
        self.image_preview = None

        # Buttons
        add_product_btn = StyledButton('Add Product', primary=True)
        add_product_btn.clicked.connect(self.addProduct)

        # Add widgets to left layout
        left_layout.addLayout(form_layout)
        left_layout.addWidget(self.image_label)
        left_layout.addWidget(add_product_btn)
        left_layout.addStretch()

        # Right panel for product list
        right_panel = QScrollArea()
        right_panel.setWidgetResizable(True)
        right_panel.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #BDBDBD;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Create a container widget for the scroll area
        scroll_container = QWidget()
        scroll_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)

        self.products_widget = QWidget()
        self.products_layout = QGridLayout(self.products_widget)
        self.products_layout.setSpacing(20)
        self.products_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add products widget to scroll container
        scroll_layout.addWidget(self.products_widget)
        scroll_layout.addStretch()
        
        # Set the scroll container as the widget for the scroll area
        right_panel.setWidget(scroll_container)

        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

    def initDatabase(self):
        try:
            # Connect to database
            conn = sqlite3.connect('products.db')
            c = conn.cursor()
            
            # Create the table with proper structure if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS products
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         product_id TEXT NOT NULL UNIQUE,
                         description TEXT,
                         category TEXT NOT NULL,
                         supplier TEXT NOT NULL,
                         quantity INTEGER NOT NULL DEFAULT 0,
                         cost REAL NOT NULL DEFAULT 0.0,
                         status TEXT NOT NULL DEFAULT 'In Stock',
                         image_data TEXT NOT NULL,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            conn.commit()
            conn.close()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            QMessageBox.critical(self, 'Database Error', f'Error initializing database: {str(e)}')

    def selectImage(self, event):
        if event.button() == Qt.LeftButton:
            files = QFileDialog.getOpenFileNames(self, 'Select Images', '', 
                                                 'Image Files (*.png *.jpg *.jpeg *.bmp *.gif)')
            if files[0]:
                self.image_path = files[0][0]
                self.image_preview = QPixmap(self.image_path)
                scaled_pixmap = self.image_preview.scaled(self.image_label.size(), 
                                                        Qt.KeepAspectRatio, 
                                                        Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)

    def image_to_base64(self, image_path):
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error converting image to base64: {str(e)}")
            return None

    def base64_to_pixmap(self, base64_string):
        try:
            image_data = base64.b64decode(base64_string)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            return pixmap
        except Exception as e:
            print(f"Error converting base64 to pixmap: {str(e)}")
            return None

    def addProduct(self):
        try:
            name = self.name_input.text().strip()
            product_id = self.product_id.text().strip()
            description = self.description_input.toPlainText().strip()
            category = self.category_combo.currentText()
            supplier = self.supplier_input.text().strip()
            quantity = self.quantity_spin.value()
            cost = self.cost_spin.value()
            status = self.status_combo.currentText()
            
            if not name:
                QMessageBox.warning(self, 'Error', 'Please enter a product name')
                return
            
            if not product_id:
                QMessageBox.warning(self, 'Error', 'Please enter a product ID')
                return
            
            if not category:
                QMessageBox.warning(self, 'Error', 'Please select a category')
                return

            if not supplier:
                QMessageBox.warning(self, 'Error', 'Please enter a supplier name')
                return

            if not self.image_path:
                QMessageBox.warning(self, 'Error', 'Please select an image')
                return

            # Convert image to base64
            image_data = self.image_to_base64(self.image_path)
            if not image_data:
                QMessageBox.critical(self, 'Error', 'Failed to process image')
                return

            # Save to database
            conn = sqlite3.connect('products.db')
            c = conn.cursor()
            
            try:
                c.execute('''INSERT INTO products 
                            (name, product_id, description, category, supplier, 
                             quantity, cost, status, image_data) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (name, product_id, description, category, supplier,
                          quantity, cost, status, image_data))
                conn.commit()

                # Also save to a JSON file for the user interface
                shop_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../SHOP'))
                if not os.path.exists(shop_dir):
                    os.makedirs(shop_dir)
                
                # Save image to SHOP/images directory
                images_dir = os.path.join(shop_dir, 'images')
                if not os.path.exists(images_dir):
                    os.makedirs(images_dir)
                
                # Copy image to SHOP/images
                image_filename = f"{product_id}.jpeg"
                image_dest = os.path.join(images_dir, image_filename)
                if self.image_path:
                    import shutil
                    shutil.copy2(self.image_path, image_dest)

                # Create or update products.json
                products_json = os.path.join(shop_dir, 'products.json')
                products = []
                if os.path.exists(products_json):
                    with open(products_json, 'r') as f:
                        products = json.load(f)

                # Add new product
                products.append({
                    'id': product_id,
                    'name': name,
                    'description': description,
                    'price': cost,
                    'image': image_filename,
                    'specs': f"Category: {category}\nSupplier: {supplier}\nStock: {quantity}",
                    'stock': quantity
                })

                # Save updated products list
                with open(products_json, 'w') as f:
                    json.dump(products, f, indent=4)

                QMessageBox.information(self, 'Success', 'Product added successfully!')
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, 'Error', 'A product with this ID already exists')
            finally:
                conn.close()

            # Clear form
            self.name_input.clear()
            self.product_id.clear()
            self.description_input.clear()
            self.supplier_input.clear()
            self.quantity_spin.setValue(0)
            self.cost_spin.setValue(0.00)
            self.image_label.setText('Drag and drop an image here\nor click to select')
            self.image_path = None
            self.image_preview = None

            # Reload products
            self.loadProducts()
        except Exception as e:
            print(f"Error adding product: {str(e)}")
            QMessageBox.critical(self, 'Error', f'An error occurred while adding the product: {str(e)}')

    def createProductCard(self, product):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                max-width: 320px;
                min-width: 280px;
            }
            QFrame:hover {
                border: 2px solid #2196F3;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transform: translateY(-2px);
            }
            QLabel {
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel[class="title"] {
                color: #1976D2;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QLabel[class="code"] {
                color: #666666;
                font-size: 13px;
                font-weight: 500;
                letter-spacing: 0.3px;
            }
            QLabel[class="price"] {
                color: #2E7D32;
                font-size: 20px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QLabel[class="quantity"] {
                color: #D32F2F;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 0.3px;
            }
            QLabel[class="status"] {
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QLabel[class="status=In Stock"] {
                background-color: #E8F5E9;
                color: #2E7D32;
            }
            QLabel[class="status=Low Stock"] {
                background-color: #FFF3E0;
                color: #EF6C00;
            }
            QLabel[class="status=Out of Stock"] {
                background-color: #FFEBEE;
                color: #C62828;
            }
            QLabel[class="category"] {
                color: #424242;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 0.3px;
            }
            QLabel[class="supplier"] {
                color: #424242;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 0.3px;
            }
            QLabel[class="description"] {
                color: #616161;
                font-size: 13px;
                line-height: 1.4;
                letter-spacing: 0.2px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
                letter-spacing: 0.5px;
            }
            QPushButton[class="delete"] {
                background-color: #FFEBEE;
                color: #C62828;
                border: 1px solid #FFCDD2;
            }
            QPushButton[class="delete"]:hover {
                background-color: #FFCDD2;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(12, 12, 12, 12)

        # Product image with shadow effect
        image_container = QFrame()
        image_container.setStyleSheet("""
            QFrame {
                background-color: #FAFAFA;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        image_label = QLabel()
        pixmap = self.base64_to_pixmap(product[9])  # image_data
        if pixmap:
            scaled_pixmap = pixmap.scaled(240, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
        else:
            image_label.setText("Image not available")
            image_label.setStyleSheet("color: #666666; padding: 20px;")
        image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(image_label)
        card_layout.addWidget(image_container)

        # Product details in a grid layout
        details_container = QFrame()
        details_layout = QGridLayout(details_container)
        details_layout.setSpacing(8)
        details_layout.setContentsMargins(0, 0, 0, 0)

        # Title and ID
        title_label = QLabel(product[1])  # name
        title_label.setProperty("class", "title")
        title_label.setWordWrap(True)
        details_layout.addWidget(title_label, 0, 0, 1, 2)

        id_label = QLabel(f"Product ID: {product[2]}")  # product_id
        id_label.setProperty("class", "code")
        details_layout.addWidget(id_label, 1, 0, 1, 2)

        # Price and Quantity
        price_label = QLabel(f"${product[7]:.2f}")  # cost
        price_label.setProperty("class", "price")
        details_layout.addWidget(price_label, 2, 0)

        quantity_label = QLabel(f"Qty: {product[6]}")  # quantity
        quantity_label.setProperty("class", "quantity")
        details_layout.addWidget(quantity_label, 2, 1)

        # Status with color coding
        status_label = QLabel(product[8])
        status_label.setProperty("class", f"status={product[8]}")
        status_label.setAlignment(Qt.AlignCenter)
        details_layout.addWidget(status_label, 3, 0, 1, 2)

        # Category and Supplier
        category_label = QLabel(f"Category: {product[4]}")
        category_label.setProperty("class", "category")
        category_label.setWordWrap(True)
        details_layout.addWidget(category_label, 4, 0, 1, 2)

        supplier_label = QLabel(f"Supplier: {product[5]}")
        supplier_label.setProperty("class", "supplier")
        supplier_label.setWordWrap(True)
        details_layout.addWidget(supplier_label, 5, 0, 1, 2)

        # Description with tooltip
        if product[3]:  # description
            desc_label = QLabel(product[3])
            desc_label.setProperty("class", "description")
            desc_label.setWordWrap(True)
            desc_label.setToolTip(product[3])
            details_layout.addWidget(desc_label, 6, 0, 1, 2)

        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setProperty("class", "delete")
        delete_btn.clicked.connect(lambda: self.deleteProduct(product[0], product[9]))
        details_layout.addWidget(delete_btn, 7, 0, 1, 2)

        card_layout.addWidget(details_container)
        return card

    def deleteProduct(self, product_id, image_data):
        try:
            reply = QMessageBox.question(self, 'Confirm Delete', 
                                    'Are you sure you want to delete this product?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                    # Get the product_id from the database first
                    conn = sqlite3.connect('products.db')
                    c = conn.cursor()
                    
                    # First verify the product exists
                    c.execute('SELECT product_id FROM products WHERE id = ?', (product_id,))
                    result = c.fetchone()
                    if not result:
                        raise Exception("Product not found in database")
                    
                    actual_product_id = result[0]
                    print(f"Deleting product with ID: {product_id}, product_id: {actual_product_id}")
                    
                    # Delete from database
                    c.execute('DELETE FROM products WHERE id = ?', (product_id,))
                    conn.commit()
                    
                    # Verify deletion
                    c.execute('SELECT COUNT(*) FROM products WHERE id = ?', (product_id,))
                    if c.fetchone()[0] > 0:
                        raise Exception("Failed to delete product from database")
                    
                    print("Successfully deleted from database")
                    conn.close()

                    # Delete from products.json
                    shop_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../SHOP'))
                    products_json = os.path.join(shop_dir, 'products.json')
                    
                    if os.path.exists(products_json):
                        with open(products_json, 'r') as f:
                            products = json.load(f)
                        
                        # Remove the product from the list
                        original_count = len(products)
                        products = [p for p in products if p['id'] != actual_product_id]
                        if len(products) == original_count:
                            print("Warning: Product not found in products.json")
                        
                        # Save updated products list
                        with open(products_json, 'w') as f:
                            json.dump(products, f, indent=4)
                        print("Successfully updated products.json")

                    # Delete the product image
                    images_dir = os.path.join(shop_dir, 'images')
                    image_path = os.path.join(images_dir, f"{actual_product_id}.jpeg")
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        print("Successfully deleted product image")
                    else:
                        print("Warning: Product image not found")

                    # Reload products to update the display
                    self.loadProducts()
                    print("Successfully reloaded products display")
                    
                    QMessageBox.information(self, 'Success', 'Product deleted successfully!')
        except Exception as e:
                print(f"Error deleting product: {str(e)}")
                QMessageBox.critical(self, 'Error', f'Error deleting product: {str(e)}')

    def loadProducts(self):
        try:
            print("Starting to load products...")
            # Clear existing products
            for i in reversed(range(self.products_layout.count())): 
                widget = self.products_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            
            # Connect to database and fetch products
            print("Connecting to database...")
            conn = sqlite3.connect('products.db')
            c = conn.cursor()
            print("Executing SELECT query...")
            c.execute('SELECT * FROM products ORDER BY created_at DESC')
            products = c.fetchall()
            print(f"Found {len(products)} products in database")
            conn.close()

            if not products:
                print("No products found, showing empty state")
                no_products_label = QLabel("No products available. Add your first product!")
                no_products_label.setStyleSheet("""
                    QLabel {
                        color: #666666;
                        font-size: 16px;
                        padding: 20px;
                        background-color: #FAFAFA;
                        border-radius: 8px;
                        border: 1px dashed #CCCCCC;
                    }
                """)
                no_products_label.setAlignment(Qt.AlignCenter)
                self.products_layout.addWidget(no_products_label)
                return

            print("Creating product cards...")
            # Create a container widget for the grid
            container = QWidget()
            grid_layout = QGridLayout(container)
            grid_layout.setSpacing(20)  # Space between cards
            grid_layout.setContentsMargins(0, 0, 0, 0)

            # Add products to grid
            row = 0
            col = 0
            max_cols = 3  # Number of products per row

            for product in products:
                print(f"Creating card for product: {product[1]}")  # product name
                card = self.createProductCard(product)
                grid_layout.addWidget(card, row, col)
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

            # Add the container widget to the products layout
            print("Adding container to layout...")
            self.products_layout.addWidget(container)
            print("Finished loading products")

        except Exception as e:
            print(f"Error loading products: {str(e)}")
            QMessageBox.critical(self, 'Error', f'Error loading products: {str(e)}')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.image_path = file
                self.image_preview = QPixmap(file)
                scaled_pixmap = self.image_preview.scaled(self.image_label.size(), 
                                                        Qt.KeepAspectRatio, 
                                                        Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                break

    def logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Import and show the login window
            login_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../LOGIN/frontend/frontend.py'))
            spec = importlib.util.spec_from_file_location('frontend', login_path)
            login_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(login_module)
            MainWindow = login_module.MainWindow
            
            # Change working directory to LOGIN directory
            os.chdir(os.path.dirname(login_path))
            
            # Show login window and close current window
            self.login_window = MainWindow()
            self.login_window.show()
            self.close()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = ProductManagerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 