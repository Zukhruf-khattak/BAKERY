from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import Product, CartOrder, SpecialOrder, ContactMessage, Feedback
from .forms import SpecialOrderForm, ContactForm, FeedbackForm, CheckoutForm, SignUpForm

# Home Page
def home(request):
    # Check for logout success message
    logout_message = request.GET.get('logout')
    if logout_message == 'success':
        messages.success(request, '✅ You have been logged out successfully! Come back soon! 🍰')
    
    best_sellers = Product.objects.filter(is_best_seller=True)[:4]
    return render(request, 'bakery/home.html', {
        'best_sellers': best_sellers
    })

# Menu Page
def menu(request):
    products = Product.objects.all()
    categories = ['cookies', 'lattes', 'waffles']
    
    category = request.GET.get('category')
    if category and category in categories:
        products = products.filter(category=category)
    
    return render(request, 'bakery/menu.html', {
        'products': products,
        'selected_category': category,
        'categories': categories
    })

# Product Detail Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'bakery/product_detail.html', {'product': product})

# Cart View
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, item in cart.items():
        product = Product.objects.get(id=int(product_id))
        subtotal = product.price * item['quantity']
        total += subtotal
        cart_items.append({
            'id': product_id,
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })
    
    return render(request, 'bakery/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

# Add to Cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'quantity': 1,
            'price': str(product.price)
        }
    
    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')

# Update Cart
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        
        if str(item_id) in cart:
            if quantity > 0:
                cart[str(item_id)]['quantity'] = quantity
            else:
                del cart[str(item_id)]
        
        request.session['cart'] = cart
        messages.success(request, 'Cart updated successfully!')
    
    return redirect('cart')

# Remove from Cart
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    
    if str(item_id) in cart:
        del cart[str(item_id)]
    
    request.session['cart'] = cart
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')

# Checkout
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('menu')
    
    cart_items = []
    total = 0
    
    for product_id, item in cart.items():
        product = Product.objects.get(id=int(product_id))
        subtotal = product.price * item['quantity']
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.items_json = json.dumps(cart)
            order.total_amount = total
            order.save()
            
            # Clear cart after order
            request.session['cart'] = {}
            
            messages.success(request, 'Order placed successfully! Thank you for shopping with us!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    
    return render(request, 'bakery/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })

# Order Confirmation
def order_confirmation(request, order_id):
    order = get_object_or_404(CartOrder, id=order_id)
    items = json.loads(order.items_json)
    
    order_items = []
    for product_id, item in items.items():
        product = Product.objects.get(id=int(product_id))
        order_items.append({
            'product': product,
            'quantity': item['quantity']
        })
    
    return render(request, 'bakery/order_confirmation.html', {
        'order': order,
        'order_items': order_items
    })

# Special Order
def special_order(request):
    if request.method == 'POST':
        form = SpecialOrderForm(request.POST)
        if form.is_valid():
            special_order = form.save()
            
            # Send email notification (optional)
            send_mail(
                f'Special Order from {special_order.name}',
                f"Name: {special_order.name}\nEmail: {special_order.email}\nPhone: {special_order.phone}\nDelivery: {special_order.delivery_option}\nItems Requested: {special_order.items_requested}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL] if settings.DEFAULT_FROM_EMAIL else ['admin@example.com'],
                fail_silently=True,
            )
            
            messages.success(request, 'Your special order has been submitted! We will contact you soon.')
            return redirect('home')
    else:
        form = SpecialOrderForm()
    
    return render(request, 'bakery/special_order.html', {'form': form})

# About Page
def about(request):
    return render(request, 'bakery/about.html')

# Contact Page
def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback! We appreciate it.')
            return redirect('contact')
    else:
        form = FeedbackForm()
    
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    return render(request, 'bakery/contact.html', {
        'form': form,
        'feedbacks': feedbacks
    })

# Sign Up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'bakery/registration/signup.html', {'form': form})

# Custom Logout Function with Message
def custom_logout(request):
    # Get username before logout
    username = request.user.username if request.user.is_authenticated else ''
    
    # Logout the user
    logout(request)
    
    # Redirect with a query parameter to show message
    return redirect('/?logout=success')