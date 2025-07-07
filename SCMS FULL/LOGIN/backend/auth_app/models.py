from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('project manager', 'Project Manager'),
        ('employee', 'Employee'),
        ('user', 'User'),
    )
    
    role = models.CharField(max_length=20, choices=ROLES, default='user')
    
    def __str__(self):
        return f"{self.username} - {self.role}"

class DeleteLog(models.Model):
    deleted_username = models.CharField(max_length=150)
    deleted_role = models.CharField(max_length=20)
    reason = models.TextField()
    deleted_at = models.DateTimeField(auto_now_add=True)
    deleted_by = models.CharField(max_length=150)  # Username of admin who deleted 

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=200)  # Store image filename
    specs = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    order_id = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id}"

class OrderItem(models.Model):
    STATUS_CHOICES = (
        ('Material', 'Material'),
        ('Manufacturing', 'Manufacturing'),
        ('Packaging', 'Packaging'),
        ('Dispatch', 'Dispatch'),
        ('Completed', 'Completed'),
    )
    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Material')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name='status_history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.order_id} - {self.status}" 