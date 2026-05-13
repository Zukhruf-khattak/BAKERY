from django.db import models
from django.contrib.auth.models import User
import os

def get_product_image_path(instance, filename):
    """Save images to category-specific folders"""
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name.replace(' ', '-').lower()}.{ext}"
    return f'products/{instance.category}/{new_filename}'

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('cookies', '🍪 Cookies'),
        ('lattes', '☕ Lattes'),
        ('waffles', '🧇 Waffles'),
        ('cakes', '🎂 Cakes'),
        ('drinks', '🥤 Drinks'),
        ('pastries', '🥐 Pastries'),    # NEW
        ('breads', '🍞 Breads'),         # NEW
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=get_product_image_path, blank=True, null=True)
    is_best_seller = models.BooleanField(default=False)
    stock = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_category_icon(self):
        icons = {
            'cookies': '🍪',
            'lattes': '☕',
            'waffles': '🧇',
            'cakes': '🎂',
            'drinks': '🥤',
            'pastries': '🥐',
            'breads': '🍞',
        }
        return icons.get(self.category, '📦')
    
    class Meta:
        ordering = ['-created_at']


class CartOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    items_json = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class SpecialOrder(models.Model):
    DELIVERY_CHOICES = [
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    delivery_option = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    items_requested = models.TextField(help_text="Describe what you want")
    special_requests = models.TextField(blank=True, null=True)
    preferred_date = models.DateField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Special Order - {self.name} ({self.submitted_at.date()})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name} - {self.created_at.date()}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    feedback = models.TextField()
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback by {self.name} - {self.rating} stars"