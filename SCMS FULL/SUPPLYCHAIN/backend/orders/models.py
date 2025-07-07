from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.FloatField()
    current_status = models.CharField(max_length=50, default="pending")

    def __str__(self):
        return self.order_id

class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    status = models.CharField(max_length=50, default="pending")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.name} ({self.quantity})"

class StatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.order.order_id} - {self.status}"
