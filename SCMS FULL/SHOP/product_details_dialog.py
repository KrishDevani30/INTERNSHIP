from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QSpinBox, QPushButton, QWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor
import os

class ProductDetailsDialog(QDialog):
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Product Details - {self.product['name']}")
        self.setMinimumWidth(600)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Product header
        header = QLabel(self.product['name'])
        header.setProperty("header", True)
        layout.addWidget(header)
        
        # Main content
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setSpacing(20)
        
        # Image section
        image_frame = QFrame()
        image_frame.setProperty("card", True)
        image_layout = QVBoxLayout(image_frame)
        
        image_label = QLabel()
        image_path = os.path.join('images', self.product['image'])
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not image_path.lower().endswith('.jpeg'):
                temp_jpeg = image_path.rsplit('.', 1)[0] + '.jpeg'
                pixmap.save(temp_jpeg, 'JPEG', quality=90)
                pixmap = QPixmap(temp_jpeg)
        else:
            pixmap = QPixmap(300, 300)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QColor('#e9ecef'))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, 300, 300)
            painter.setPen(QColor('#495057'))
            font = QFont('Arial', 60, QFont.Bold)
            painter.setFont(font)
            initials = ''.join(word[0].upper() for word in self.product['name'].split()[:2])
            painter.drawText(pixmap.rect(), Qt.AlignCenter, initials)
            painter.end()
        
        scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
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
        
        # Product ID
        if 'id' in self.product:
            id_label = QLabel(f"Product ID: {self.product['id']}")
            id_label.setProperty("specs", True)
            details_layout.addWidget(id_label)
        
        # Category
        if 'category' in self.product:
            category_label = QLabel(f"Category: {self.product['category']}")
            category_label.setProperty("specs", True)
            details_layout.addWidget(category_label)
        
        # Specifications
        if 'specs' in self.product:
            specs_label = QLabel(f"Specifications:\n{self.product['specs']}")
            specs_label.setProperty("specs", True)
            specs_label.setWordWrap(True)
            details_layout.addWidget(specs_label)
        
        # Stock information
        if 'stock' in self.product:
            stock_label = QLabel(f"Available Stock: {self.product['stock']} units")
            stock_label.setProperty("specs", True)
            details_layout.addWidget(stock_label)
        
        # Supplier information
        if 'supplier' in self.product:
            supplier_label = QLabel(f"Supplier: {self.product['supplier']}")
            supplier_label.setProperty("specs", True)
            details_layout.addWidget(supplier_label)
        
        # Add to cart section
        cart_frame = QFrame()
        cart_frame.setObjectName("cart_frame")
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