from django.contrib import admin
from .models import Product, CartOrder, SpecialOrder, ContactMessage, Feedback, Profile

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_best_seller']
    list_filter = ['category', 'is_best_seller']
    search_fields = ['name']
    list_editable = ['price', 'stock', 'is_best_seller']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'email']
    list_editable = ['status']

class SpecialOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'delivery_option', 'submitted_at']
    list_filter = ['delivery_option', 'submitted_at']
    search_fields = ['name', 'email']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile', 'address']
    search_fields = ['user__username', 'mobile']

admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(SpecialOrder, SpecialOrderAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Profile, ProfileAdmin)