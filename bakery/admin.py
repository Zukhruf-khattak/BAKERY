from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, CartOrder, SpecialOrder, ContactMessage, Feedback
import json

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'is_best_seller', 'stock']
    list_filter = ['category', 'is_best_seller']
    search_fields = ['name']
    list_editable = ['price', 'is_best_seller', 'stock']
    list_per_page = 20

@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'display_items']
    list_per_page = 20
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'email', 'phone')
        }),
        ('Shipping Information', {
            'fields': ('address', 'city', 'zip_code')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'status')
        }),
        ('🛒 Cart Items', {
            'fields': ('display_items',),
            'classes': ('wide',),
        }),
        ('Additional Info', {
            'fields': ('user', 'created_at')
        }),
    )
    
    def display_items(self, obj):
        """Display cart items in a readable format"""
        try:
            items = json.loads(obj.items_json)
            
            if not items:
                return "No items in cart"
            
            # Simple text format (no HTML)
            lines = []
            lines.append("=" * 50)
            lines.append(f"{'Product':<30} {'Qty':>5} {'Price':>8} {'Total':>8}")
            lines.append("=" * 50)
            
            total = 0
            if isinstance(items, list):
                # New array format
                for item in items:
                    item_total = float(item['price']) * int(item['quantity'])
                    total += item_total
                    lines.append(f"{item['name']:<30} {item['quantity']:>5} ${float(item['price']):>7.2f} ${item_total:>7.2f}")
            else:
                # Old object format
                for item_id, item in items.items():
                    item_total = float(item['price']) * int(item['quantity'])
                    total += item_total
                    lines.append(f"{item['name']:<30} {item['quantity']:>5} ${float(item['price']):>7.2f} ${item_total:>7.2f}")
            
            lines.append("=" * 50)
            lines.append(f"{'GRAND TOTAL':<30} {'':>5} {'':>8} ${total:>7.2f}")
            lines.append("=" * 50)
            
            return mark_safe(f'<pre style="background-color:#f5f5f5; padding:15px; border-radius:5px; font-family:monospace;">{"<br>".join(lines)}</pre>')
            
        except Exception as e:
            return f"Error loading cart items: {str(e)}"
    
    display_items.short_description = '🛒 Cart Contents'
    display_items.allow_tags = True

@admin.register(SpecialOrder)
class SpecialOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'delivery_option', 'submitted_at', 'is_processed']
    list_filter = ['delivery_option', 'submitted_at', 'is_processed']
    search_fields = ['name', 'email', 'items_requested']
    list_editable = ['is_processed']
    list_per_page = 20

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_filter = ['created_at', 'is_read']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']
    list_per_page = 20

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['name', 'feedback']
    list_per_page = 20