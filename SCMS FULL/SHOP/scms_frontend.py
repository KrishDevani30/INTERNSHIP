import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QSpinBox, QPushButton,
                            QScrollArea, QGridLayout, QLineEdit, QMessageBox,
                            QFrame, QDialog, QFormLayout, QTextEdit)
from PyQt5.QtCore import Qt, QSize, QByteArray, QPoint
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QPainter, QPainterPath
from product_details_dialog import ProductDetailsDialog
import requests
import importlib

class ProductDetailsDialog(QDialog):
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Product Details - {self.product['name']}")
        self.setMinimumWidth(600)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #333333;
            }
            QFrame#image_container {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Product header
        header = QLabel(self.product['name'])
        header.setProperty("header", True)
        header.setStyleSheet("""
            QLabel[header="true"] {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(header)
        
        # Main content
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Image section
        image_frame = QFrame()
        image_frame.setObjectName("image_container")
        image_frame.setFixedSize(400, 400)
        image_layout = QVBoxLayout(image_frame)
        image_layout.setContentsMargins(10, 10, 10, 10)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border-radius: 15px;
            }
        """)
        
        image_path = os.path.join('images', self.product['image'])
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not image_path.lower().endswith('.jpeg'):
                temp_jpeg = image_path.rsplit('.', 1)[0] + '.jpeg'
                pixmap.save(temp_jpeg, 'JPEG', quality=95)
                pixmap = QPixmap(temp_jpeg)
            
            # Scale image while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                380, 380,  # Slightly smaller than container to allow for padding
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Create a rounded pixmap with shadow
            rounded_pixmap = QPixmap(380, 380)
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw shadow
            shadow = QPainterPath()
            shadow.addRoundedRect(4, 4, 372, 372, 15, 15)
            painter.fillPath(shadow, QColor(0, 0, 0, 30))
            
            # Draw image
            path = QPainterPath()
            path.addRoundedRect(0, 0, 380, 380, 15, 15)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            image_label.setPixmap(rounded_pixmap)
        else:
            # Create placeholder with initials
            pixmap = QPixmap(380, 380)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw background circle
            painter.setBrush(QColor('#f8f9fa'))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, 380, 380)
            
            # Draw initials
            painter.setPen(QColor('#495057'))
            font = QFont('Arial', 72, QFont.Bold)
            painter.setFont(font)
            initials = ''.join(word[0].upper() for word in self.product['name'].split()[:2])
            painter.drawText(pixmap.rect(), Qt.AlignCenter, initials)
            painter.end()
            
            image_label.setPixmap(pixmap)
        
        image_layout.addWidget(image_label)
        content_layout.addWidget(image_frame)
        
        # Details section
        details_frame = QFrame()
        details_frame.setProperty("card", True)
        details_layout = QVBoxLayout(details_frame)
        details_layout.setSpacing(15)
        
        # Price
        price_label = QLabel(f"${self.product['price']:.2f}")
        price_label.setProperty("price", True)
        details_layout.addWidget(price_label)
        
        # Description
        desc_label = QLabel(self.product['description'])
        desc_label.setWordWrap(True)
        details_layout.addWidget(desc_label)
        
        # Specifications
        if 'specs' in self.product:
            specs_label = QLabel(f"Specifications:\n{self.product['specs']}")
            specs_label.setWordWrap(True)
            details_layout.addWidget(specs_label)
        
        # Add to cart section
        cart_frame = QFrame()
        cart_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: none;
            }
        """)
        cart_layout = QHBoxLayout(cart_frame)
        
        quantity_label = QLabel('Quantity:')
        quantity_spinner = QSpinBox()
        quantity_spinner.setMinimum(1)
        quantity_spinner.setMaximum(99)
        quantity_spinner.setValue(1)
        
        cart_layout.addWidget(quantity_label)
        cart_layout.addWidget(quantity_spinner)
        cart_layout.addStretch()
        
        add_button = QPushButton('Add to Cart')
        add_button.clicked.connect(lambda: self.add_to_cart(quantity_spinner.value()))
        cart_layout.addWidget(add_button)
        
        details_layout.addWidget(cart_frame)
        content_layout.addWidget(details_frame)
        
        layout.addWidget(content)
        
        # Close button
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

    def add_to_cart(self, quantity):
        if self.parent():
            self.parent().add_to_cart(self.product, quantity)
        self.accept()

class CartWindow(QDialog):
    def __init__(self, cart, parent=None, update_cart_callback=None, checkout_callback=None):
        super().__init__(parent)
        self.cart = cart
        self.update_cart_callback = update_cart_callback
        self.checkout_callback = checkout_callback
        self.setWindowTitle('Shopping Cart')
        self.setMinimumWidth(500)
        self.setStyleSheet('''
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel[header="true"] {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel[price="true"] {
                color: #2ecc71;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QFrame[card="true"] {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 10px;
            }
        ''')
        self.item_widgets = {}  # Store widgets for each item
        self.init_ui()

    def init_ui(self):
        self.layout_ = QVBoxLayout(self)
        self.layout_.setSpacing(20)
        self.layout_.setContentsMargins(20, 20, 20, 20)

        header = QLabel('Shopping Cart')
        header.setProperty("header", True)
        self.layout_.addWidget(header)

        self.item_widgets.clear()
        self.cards = []

        # Cart items
        if not self.cart:
            self.empty_label = QLabel('Your cart is empty.')
            self.empty_label.setAlignment(Qt.AlignCenter)
            self.layout_.addWidget(self.empty_label)
        else:
            for item in self.cart.values():
                card = QFrame()
                card.setProperty("card", True)
                card_layout = QHBoxLayout(card)
                card_layout.setSpacing(10)
                card_layout.setContentsMargins(10, 10, 10, 10)

                name_label = QLabel(item['name'])
                name_label.setMinimumWidth(120)
                card_layout.addWidget(name_label)

                qty_label = QLabel(f"× {item['quantity']}")
                card_layout.addWidget(qty_label)

                price_label = QLabel(f"${item['price'] * item['quantity']:.2f}")
                price_label.setProperty("price", True)
                card_layout.addWidget(price_label)

                # Remove button
                remove_btn = QPushButton('Remove')
                remove_btn.clicked.connect(lambda _, i=item: self.remove_item(i))
                card_layout.addWidget(remove_btn)

                self.layout_.addWidget(card)
                self.item_widgets[item['id']] = {
                    'card': card,
                    'qty_label': qty_label,
                    'price_label': price_label
                }
                self.cards.append(card)

        # Total
        self.total_label = QLabel(f"Total: ${self.calculate_total():.2f}")
        self.total_label.setProperty("price", True)
        self.total_label.setAlignment(Qt.AlignRight)
        self.layout_.addWidget(self.total_label)

        # Checkout button
        if self.cart:
            self.checkout_btn = QPushButton('Proceed to Checkout')
            self.checkout_btn.clicked.connect(self.checkout)
            self.layout_.addWidget(self.checkout_btn)

        # Close button
        self.close_btn = QPushButton('Close')
        self.close_btn.clicked.connect(self.accept)
        self.layout_.addWidget(self.close_btn)

    def calculate_total(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def remove_item(self, item):
        item_id = item['id']
        if item_id in self.cart:
            if self.cart[item_id]['quantity'] > 1:
                self.cart[item_id]['quantity'] -= 1
                # Update only the quantity and price label
                w = self.item_widgets[item_id]
                w['qty_label'].setText(f"× {self.cart[item_id]['quantity']}")
                w['price_label'].setText(f"${self.cart[item_id]['price'] * self.cart[item_id]['quantity']:.2f}")
            else:
                # Remove the card from UI
                w = self.item_widgets[item_id]
                w['card'].setParent(None)
                del self.cart[item_id]
                del self.item_widgets[item_id]
            # Update total
            self.total_label.setText(f"Total: ${self.calculate_total():.2f}")
            if self.update_cart_callback:
                self.update_cart_callback()
            # If cart is empty after removal, show empty label and hide checkout
            if not self.cart:
                self.empty_label = QLabel('Your cart is empty.')
                self.empty_label.setAlignment(Qt.AlignCenter)
                self.layout_.insertWidget(1, self.empty_label)
                if hasattr(self, 'checkout_btn'):
                    self.checkout_btn.hide()

    def checkout(self):
        if self.checkout_callback:
            self.accept()
            self.checkout_callback()

class SCMSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cart = {}  # Dictionary to store cart items with product id as key
        self.cart_items_widget = None
        self.cart_items_layout = None
        self.total_label = None
        self.products_grid = None
        self.products_grid_layout = None
        self.current_user = None  # Store current user
        self.load_stylesheet()
        self.init_ui()
        self.load_products()

    def showEvent(self, event):
        """Override showEvent to refresh products when window is shown"""
        super().showEvent(event)
        self.load_products()  # Refresh products when window is shown

    def load_stylesheet(self):
        qss_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.qss')
        if os.path.exists(qss_file):
            with open(qss_file, 'r') as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Warning: QSS file not found at {qss_file}")

    def init_ui(self):
        self.setWindowTitle('SHOP')
        self.setMinimumSize(1200, 800)
        
        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Top bar with cart button
        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel('SHOP')
        title_label.setProperty("header", True)
        title_label.setStyleSheet("""
            QLabel[header="true"] {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        top_layout.addWidget(title_label)
        
        # Add stretch to push buttons to the right
        top_layout.addStretch()
        
        # History button
        self.history_button = QPushButton('📋')
        self.history_button.setProperty("cart", True)
        self.history_button.setStyleSheet("""
            QPushButton[cart="true"] {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 24px;
                padding: 5px;
            }
            QPushButton[cart="true"]:hover {
                background-color: #27ae60;
            }
        """)
        self.history_button.clicked.connect(self.show_order_history)
        self.history_button.setFixedSize(50, 50)
        top_layout.addWidget(self.history_button)
        
        # Cart container
        cart_container = QWidget()
        cart_container_layout = QHBoxLayout(cart_container)
        cart_container_layout.setSpacing(30)
        cart_container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Cart button with counter
        cart_button_container = QWidget()
        cart_button_layout = QHBoxLayout(cart_button_container)
        cart_button_layout.setContentsMargins(0, 0, 0, 0)
        cart_button_layout.setSpacing(5)
        
        # Cart button
        self.cart_button = QPushButton('🛒')
        self.cart_button.setProperty("cart", True)
        self.cart_button.setStyleSheet("""
            QPushButton[cart="true"] {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 24px;
                padding: 5px;
            }
            QPushButton[cart="true"]:hover {
                background-color: #2980b9;
            }
        """)
        self.cart_button.clicked.connect(self.toggle_cart)
        self.cart_button.setFixedSize(50, 50)
        
        # Cart items counter
        self.cart_counter = QLabel('0')
        self.cart_counter.setProperty("cart_counter", True)
        self.cart_counter.setStyleSheet("""
            QLabel[cart_counter="true"] {
                background-color: #e74c3c;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
                padding: 5px 10px;
                min-width: 25px;
                min-height: 25px;
            }
        """)
        self.cart_counter.setAlignment(Qt.AlignCenter)
        self.cart_counter.setFixedSize(25, 25)
        
        cart_button_layout.addWidget(self.cart_button)
        cart_button_layout.addWidget(self.cart_counter)
        
        cart_container_layout.addWidget(cart_button_container)
        
        # Logout button
        self.logout_button = QPushButton('🚪')
        self.logout_button.setProperty("cart", True)
        self.logout_button.setStyleSheet("""
            QPushButton[cart="true"] {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 24px;
                padding: 5px;
            }
            QPushButton[cart="true"]:hover {
                background-color: #c0392b;
            }
        """)
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setFixedSize(50, 50)
        cart_container_layout.addWidget(self.logout_button)
        
        top_layout.addWidget(cart_container)
        main_layout.addWidget(top_bar)

        # Content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Products section
        products_widget = QFrame()
        products_widget.setProperty("card", True)
        products_widget.setStyleSheet("""
            QFrame[card="true"] {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        """)
        products_layout = QVBoxLayout(products_widget)
        products_layout.setContentsMargins(20, 20, 20, 20)
        products_layout.setSpacing(20)
        
        # Products header
        products_header = QLabel('Available Products')
        products_header.setProperty("header", True)
        products_header.setStyleSheet("""
            QLabel[header="true"] {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        products_layout.addWidget(products_header)

        # Products grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.products_grid = QWidget()
        self.products_grid_layout = QGridLayout(self.products_grid)
        self.products_grid_layout.setSpacing(30)
        self.products_grid_layout.setContentsMargins(10, 10, 10, 10)
        scroll.setWidget(self.products_grid)
        products_layout.addWidget(scroll)

        # Cart section
        self.cart_widget = QFrame()
        self.cart_widget.setProperty("card", True)
        self.cart_widget.setMaximumWidth(400)
        self.cart_widget.hide()  # Initially hidden
        cart_layout = QVBoxLayout(self.cart_widget)
        cart_layout.setContentsMargins(20, 20, 20, 20)
        cart_layout.setSpacing(15)
        
        # Cart header
        cart_header = QLabel('Shopping Cart')
        cart_header.setProperty("header", True)
        cart_layout.addWidget(cart_header)

        # Cart items
        cart_scroll = QScrollArea()
        cart_scroll.setWidgetResizable(True)
        
        self.cart_items_widget = QWidget()
        self.cart_items_layout = QVBoxLayout(self.cart_items_widget)
        self.cart_items_layout.setSpacing(10)
        self.cart_items_layout.setContentsMargins(0, 0, 0, 0)
        cart_scroll.setWidget(self.cart_items_widget)
        cart_layout.addWidget(cart_scroll)

        # Total amount
        self.total_label = QLabel('Total: $0.00')
        self.total_label.setProperty("price", True)
        cart_layout.addWidget(self.total_label)

        # Checkout button
        checkout_btn = QPushButton('Proceed to Checkout')
        checkout_btn.clicked.connect(self.show_checkout_form)
        cart_layout.addWidget(checkout_btn)

        # Add sections to content layout
        content_layout.addWidget(products_widget, stretch=2)
        content_layout.addWidget(self.cart_widget, stretch=1)
        
        main_layout.addWidget(content_widget)

    def load_products(self):
        try:
            # Load products from JSON file
                products_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products.json')
                if os.path.exists(products_json):
                    with open(products_json, 'r') as f:
                        products = json.load(f)
                else:
                    products = []

                row = 0
                col = 0
                max_cols = 3  # Maximum number of products per row
                for product in products:
                    product_card = self.create_product_card(product)
                    self.products_grid_layout.addWidget(product_card, row, col)
                    col += 1
                    if col == max_cols:
                        col = 0
                        row += 1
        except Exception as e:
            print(f"Error loading products: {str(e)}")
            QMessageBox.critical(self, 'Error', f'Failed to load products: {str(e)}')

    def create_product_card(self, product):
        card = QFrame()
        card.setProperty("card", True)
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("""
            QFrame[card="true"] {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
            QFrame[card="true"]:hover {
                border: 1px solid #3498db;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
        """)
        card.mousePressEvent = lambda e: self.show_product_details(product)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Product image container with shadow effect
        image_container = QFrame()
        image_container.setObjectName("image_container")
        image_container.setFixedSize(250, 250)
        image_container.setStyleSheet("""
            QFrame#image_container {
                background-color: white;
                border-radius: 125px;
                border: 1px solid #e0e0e0;
            }
        """)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        # Product image
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border-radius: 125px;
            }
        """)
        
        image_path = os.path.join('images', product['image'])
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not image_path.lower().endswith('.jpeg'):
                temp_jpeg = image_path.rsplit('.', 1)[0] + '.jpeg'
                pixmap.save(temp_jpeg, 'JPEG', quality=95)
                pixmap = QPixmap(temp_jpeg)
            
            # Scale image while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                230, 230,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Create a circular pixmap with shadow
            rounded_pixmap = QPixmap(230, 230)
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw shadow
            shadow = QPainterPath()
            shadow.addEllipse(2, 2, 226, 226)
            painter.fillPath(shadow, QColor(0, 0, 0, 30))
            
            # Draw image
            path = QPainterPath()
            path.addEllipse(0, 0, 230, 230)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            image_label.setPixmap(rounded_pixmap)
        else:
            # Create circular placeholder with initials
            pixmap = QPixmap(230, 230)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw background circle
            painter.setBrush(QColor('#f8f9fa'))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, 230, 230)
            
            # Draw initials
            painter.setPen(QColor('#495057'))
            font = QFont('Arial', 46, QFont.Bold)
            painter.setFont(font)
            initials = ''.join(word[0].upper() for word in product['name'].split()[:2])
            painter.drawText(pixmap.rect(), Qt.AlignCenter, initials)
            painter.end()
            
            image_label.setPixmap(pixmap)
        
        image_layout.addWidget(image_label)
        layout.addWidget(image_container)
        
        # Product name
        name_label = QLabel(product['name'])
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                font-size: 16px;
            }
        """)
        layout.addWidget(name_label)
        
        # Product price
        price_label = QLabel(f"${product['price']:.2f}")
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setProperty("price", True)
        price_label.setStyleSheet("""
            QLabel[price="true"] {
                color: #2ecc71;
                font-weight: bold;
                font-size: 18px;
            }
        """)
        layout.addWidget(price_label)
        
        return card

    def create_cart_item(self, item):
        item_widget = QFrame()
        item_widget.setObjectName("cart_item")
        item_widget.setProperty("card", True)
        
        layout = QVBoxLayout(item_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Item name
        name_label = QLabel(item['name'])
        layout.addWidget(name_label)
        
        # Item details container
        details_container = QFrame()
        details_container.setObjectName("cart_frame")
        details_layout = QVBoxLayout(details_container)
        details_layout.setContentsMargins(10, 10, 10, 10)
        details_layout.setSpacing(5)
        
        # Quantity and price
        details_label = QLabel(f"Quantity: {item['quantity']} × ${item['price']:.2f}")
        details_layout.addWidget(details_label)
        
        # Subtotal
        subtotal = item['quantity'] * item['price']
        subtotal_label = QLabel(f"Subtotal: ${subtotal:.2f}")
        subtotal_label.setProperty("price", True)
        details_layout.addWidget(subtotal_label)
        
        layout.addWidget(details_container)
        
        # Remove button
        remove_btn = QPushButton('Remove')
        remove_btn.setObjectName("remove_btn")
        item_id = item['id']
        remove_btn.clicked.connect(lambda: self.remove_from_cart({'id': item_id}))
        layout.addWidget(remove_btn)
        
        return item_widget

    def add_to_cart(self, product, quantity):
        product_id = product['id']
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity
            }
        
        self.update_cart_display()

    def update_cart_display(self):
        # Clear existing items
        while self.cart_items_layout.count():
            item = self.cart_items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add updated items
        for item in self.cart.values():
            item_widget = self.create_cart_item(item)
            self.cart_items_layout.addWidget(item_widget)
        
        # Update total
        self.total_label.setText(f"Total: ${self.calculate_total():.2f}")
        
        # Update cart counter
        total_items = sum(item['quantity'] for item in self.cart.values())
        self.cart_counter.setText(str(total_items))

    def remove_from_cart(self, item):
        product_id = item['id']
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                # Decrease quantity by 1
                self.cart[product_id]['quantity'] -= 1
            else:
                # Remove the item if quantity is 1
                del self.cart[product_id]
            self.update_cart_display()

    def show_checkout_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Checkout')
        dialog.setMinimumWidth(600)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        
        # Form fields container
        fields_container = QFrame()
        fields_container.setObjectName("fields_container")
        fields_layout = QFormLayout(fields_container)
        fields_layout.setSpacing(15)
        
        # Form fields
        name_edit = QLineEdit()
        email_edit = QLineEdit()
        phone_edit = QLineEdit()  # Added phone field
        address_edit = QTextEdit()
        address_edit.setMaximumHeight(100)
        
        fields_layout.addRow('Full Name:', name_edit)
        fields_layout.addRow('Email:', email_edit)
        fields_layout.addRow('Phone:', phone_edit)  # Added phone field
        fields_layout.addRow('Shipping Address:', address_edit)
        
        # Required fields note
        required_note = QLabel('* All fields are required')
        required_note.setObjectName("required_note")
        fields_layout.addRow('', required_note)
        
        layout.addWidget(fields_container)
        
        # Order items container
        items_container = QFrame()
        items_container.setObjectName("items_container")
        items_layout = QVBoxLayout(items_container)
        items_layout.setSpacing(10)
        
        # Add items to container
        for item in self.cart.values():
            item_widget = QFrame()
            item_widget.setObjectName("item_widget")
            item_layout = QHBoxLayout(item_widget)
            
            name_label = QLabel(f"{item['name']} × {item['quantity']}")
            price_label = QLabel(f"${item['price'] * item['quantity']:.2f}")
            price_label.setProperty("price", True)
            
            item_layout.addWidget(name_label)
            item_layout.addWidget(price_label)
            
            items_layout.addWidget(item_widget)
        
        layout.addWidget(items_container)
        
        # Total amount
        total_label = QLabel(f"Total: ${self.calculate_total():.2f}")
        total_label.setProperty("price", True)
        layout.addWidget(total_label)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(dialog.reject)
        
        submit_btn = QPushButton('Place Order')
        submit_btn.clicked.connect(lambda: self.process_order(
            name_edit.text(),
            email_edit.text(),
            phone_edit.text(),  # Added phone
            address_edit.toPlainText(),
            dialog
        ))
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(submit_btn)
        
        layout.addLayout(buttons_layout)
        
        dialog.exec_()

    def calculate_total(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def process_order(self, name, email, phone, address, dialog):
        # Validate inputs
        if not name or not email or not phone or not address:
            QMessageBox.warning(
                self, 
                'Incomplete Information',
                'Please fill in all the required fields.',
                QMessageBox.Ok
            )
            return
        
        try:
            # Create orders directory if it doesn't exist
            if not os.path.exists('orders'):
                os.makedirs('orders')
            
            # Generate unique order ID with timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            order_id = f"ORDER_{timestamp}"
            
            # Prepare order data
            order_data = {
                'order_id': order_id,
                'timestamp': datetime.datetime.now().isoformat(),
                'username': self.current_user,  # Add username to order data
                'customer': {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'address': address
                },
                'items': list(self.cart.values()),
                'total': self.calculate_total(),
                'status': 'pending',
                'status_history': [
                    {
                        'status': 'pending',
                        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'notes': 'Order created'
                    }
                ]
            }
            
            # Save order to file
            order_file = os.path.join('orders', f"{order_id}.json")
            with open(order_file, 'w') as f:
                json.dump(order_data, f, indent=4)

            # --- Automatic import to backend ---
            try:
                response = requests.post(
                    'http://localhost:8000/api/load_order/',
                    json=order_data
                )
                if response.status_code in [200, 201]:
                    print('Order loaded into backend successfully.')
                else:
                    print('Failed to load order into backend:', response.text)
            except Exception as e:
                print('Error sending order to backend:', e)
            # --- End automatic import ---
            
            # Clear cart and close dialog
            self.cart.clear()
            self.update_cart_display()
            dialog.accept()
            
            # Show success message
            QMessageBox.information(
                self, 
                'Order Placed',
                f'Your order has been placed successfully!\nOrder ID: {order_id}',
                QMessageBox.Ok
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                'Error',
                f'An error occurred while processing your order:\n{str(e)}',
                QMessageBox.Ok
            )

    def toggle_cart(self):
        # Open cart in a new window/dialog with enhanced UI
        dialog = CartWindow(self.cart, parent=self, update_cart_callback=self.update_cart_display, checkout_callback=self.show_checkout_form)
        dialog.exec_()

    def show_product_details(self, product):
        dialog = ProductDetailsDialog(product, self)
        dialog.exec_()

    def logout(self):
        try:
            response = requests.post('http://localhost:8000/api/logout/')
            if response.status_code == 200:
                # Close the shop window
                self.close()
                # Reopen the login window
                login_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../LOGIN/frontend/frontend.py'))
                spec = importlib.util.spec_from_file_location('frontend', login_path)
                login_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(login_module)
                MainWindow = login_module.MainWindow
                login_window = MainWindow()
                login_window.show()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to logout: {str(e)}')

    def show_order_history(self):
        if not self.current_user:
            QMessageBox.warning(
                self,
                'Error',
                'Please log in to view your order history.',
                QMessageBox.Ok
            )
            return

        # Create order history window
        history_window = QDialog(self)
        history_window.setWindowTitle('My Order History')
        history_window.setMinimumSize(1000, 700)
        history_window.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel[price="true"] {
                color: #2ecc71;
                font-weight: bold;
                font-size: 16px;
            }
        """)
        
        layout = QVBoxLayout(history_window)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        # Title and user info
        title_layout = QHBoxLayout()
        title_label = QLabel(f'Order History')
        title_label.setProperty("header", True)
        title_label.setStyleSheet("""
            QLabel[header="true"] {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        
        user_label = QLabel(f'Welcome, {self.current_user}')
        user_label.setStyleSheet("""
            color: #7f8c8d;
            font-size: 16px;
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(user_label)
        
        header_layout.addLayout(title_layout)
        layout.addWidget(header_frame)
        
        # Orders container
        orders_container = QScrollArea()
        orders_container.setWidgetResizable(True)
        orders_container.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        orders_widget = QWidget()
        orders_layout = QVBoxLayout(orders_widget)
        orders_layout.setSpacing(20)
        orders_layout.setContentsMargins(0, 0, 0, 0)
        
        # Load and display orders
        if os.path.exists('orders'):
            order_files = sorted(os.listdir('orders'), reverse=True)
            has_orders = False
            
            for order_file in order_files:
                try:
                    with open(os.path.join('orders', order_file), 'r') as f:
                        order_data = json.load(f)
                    
                    # Only show orders for current user
                    if order_data.get('username') != self.current_user:
                        continue
                    
                    has_orders = True
                    
                    # Create order card
                    order_card = QFrame()
                    order_card.setProperty("card", True)
                    order_card.setStyleSheet("""
                        QFrame[card="true"] {
                            background-color: white;
                            border-radius: 15px;
                            border: 1px solid #e0e0e0;
                        }
                        QFrame[card="true"]:hover {
                            border: 1px solid #3498db;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        }
                    """)
                    
                    card_layout = QVBoxLayout(order_card)
                    card_layout.setSpacing(15)
                    card_layout.setContentsMargins(20, 20, 20, 20)
                    
                    # Order header
                    header_layout = QHBoxLayout()
                    
                    # Left side: Order ID and Date
                    left_info = QVBoxLayout()
                    order_id_label = QLabel(f"Order #{order_data['order_id'].split('_')[1]}")
                    order_id_label.setStyleSheet("""
                        font-weight: bold;
                        font-size: 18px;
                        color: #2c3e50;
                    """)
                    date_label = QLabel(f"Placed on {order_data['timestamp'].split('T')[0]}")
                    date_label.setStyleSheet("color: #7f8c8d;")
                    left_info.addWidget(order_id_label)
                    left_info.addWidget(date_label)
                    
                    # Right side: Status
                    status_frame = QFrame()
                    status_frame.setStyleSheet("""
                        QFrame {
                            background-color: #e8f5e9;
                            border-radius: 5px;
                            padding: 5px 10px;
                        }
                    """)
                    status_layout = QHBoxLayout(status_frame)
                    status_layout.setContentsMargins(10, 5, 10, 5)
                    status_label = QLabel(f"Status: {order_data['status'].title()}")
                    status_label.setStyleSheet("""
                        color: #2ecc71;
                        font-weight: bold;
                    """)
                    status_layout.addWidget(status_label)
                    
                    header_layout.addLayout(left_info)
                    header_layout.addStretch()
                    header_layout.addWidget(status_frame)
                    
                    card_layout.addLayout(header_layout)
                    
                    # Separator line
                    line = QFrame()
                    line.setFrameShape(QFrame.HLine)
                    line.setStyleSheet("background-color: #e0e0e0;")
                    card_layout.addWidget(line)
                    
                    # Order items
                    items_label = QLabel("Order Items")
                    items_label.setStyleSheet("""
                        font-weight: bold;
                        font-size: 16px;
                        color: #2c3e50;
                        margin-top: 10px;
                    """)
                    card_layout.addWidget(items_label)
                    
                    # Items container
                    items_container = QFrame()
                    items_container.setStyleSheet("""
                        QFrame {
                            background-color: #f8f9fa;
                            border-radius: 10px;
                            padding: 15px;
                        }
                    """)
                    items_layout = QVBoxLayout(items_container)
                    items_layout.setSpacing(10)
                    
                    for item in order_data['items']:
                        item_widget = QFrame()
                        item_widget.setStyleSheet("""
                            QFrame {
                                background-color: white;
                                border-radius: 5px;
                                padding: 10px;
                            }
                        """)
                        item_layout = QHBoxLayout(item_widget)
                        
                        item_name = QLabel(f"{item['name']}")
                        item_name.setStyleSheet("font-weight: bold;")
                        item_quantity = QLabel(f"× {item['quantity']}")
                        item_quantity.setStyleSheet("color: #7f8c8d;")
                        item_price = QLabel(f"${item['price'] * item['quantity']:.2f}")
                        item_price.setProperty("price", True)
                        
                        item_layout.addWidget(item_name)
                        item_layout.addWidget(item_quantity)
                        item_layout.addStretch()
                        item_layout.addWidget(item_price)
                        
                        items_layout.addWidget(item_widget)
                    
                    card_layout.addWidget(items_container)
                    
                    # Total
                    total_frame = QFrame()
                    total_frame.setStyleSheet("""
                        QFrame {
                            background-color: #f8f9fa;
                            border-radius: 10px;
                            padding: 15px;
                        }
                    """)
                    total_layout = QHBoxLayout(total_frame)
                    total_label = QLabel("Total Amount:")
                    total_label.setStyleSheet("font-weight: bold; font-size: 16px;")
                    total_amount = QLabel(f"${order_data['total']:.2f}")
                    total_amount.setProperty("price", True)
                    
                    total_layout.addWidget(total_label)
                    total_layout.addStretch()
                    total_layout.addWidget(total_amount)
                    
                    card_layout.addWidget(total_frame)
                    
                    orders_layout.addWidget(order_card)
                    
                except Exception as e:
                    print(f"Error loading order {order_file}: {str(e)}")
            
            if not has_orders:
                no_orders_frame = QFrame()
                no_orders_frame.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border-radius: 15px;
                        padding: 40px;
                    }
                """)
                no_orders_layout = QVBoxLayout(no_orders_frame)
                
                no_orders_label = QLabel("You haven't placed any orders yet.")
                no_orders_label.setStyleSheet("""
                    color: #7f8c8d;
                    font-size: 18px;
                    font-weight: bold;
                """)
                no_orders_label.setAlignment(Qt.AlignCenter)
                
                shop_now_label = QLabel("Start shopping to see your orders here!")
                shop_now_label.setStyleSheet("""
                    color: #95a5a6;
                    font-size: 14px;
                """)
                shop_now_label.setAlignment(Qt.AlignCenter)
                
                no_orders_layout.addWidget(no_orders_label)
                no_orders_layout.addWidget(shop_now_label)
                
                orders_layout.addWidget(no_orders_frame)
        
        orders_container.setWidget(orders_widget)
        layout.addWidget(orders_container)
        
        # Close button
        close_button = QPushButton('Close')
        close_button.setFixedWidth(200)
        close_button.clicked.connect(history_window.accept)
        
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        layout.addWidget(button_container)
        
        history_window.exec_()

    def set_current_user(self, username):
        self.current_user = username

def main():
    app = QApplication(sys.argv)
    window = SCMSApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 