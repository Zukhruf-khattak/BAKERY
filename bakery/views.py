from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, CartOrder, SpecialOrder, ContactMessage, Feedback
from .forms import ContactForm, FeedbackForm, SpecialOrderForm
import json
from decimal import Decimal

def home(request):
    best_sellers = Product.objects.filter(is_best_seller=True)[:6]
    return render(request, 'bakery/home.html', {'best_sellers': best_sellers})

def menu(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    return render(request, 'bakery/menu.html', {'products': products})

def about(request):
    return render(request, 'bakery/about.html')

def contact(request):
    if request.method == 'POST':
        if 'contact_submit' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            
            if name and email and message:
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    message=message
                )
                messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
            else:
                messages.error(request, 'Please fill all fields.')
        
        elif 'feedback_submit' in request.POST:
            name = request.POST.get('feedback_name')
            rating = request.POST.get('rating')
            feedback_text = request.POST.get('feedback')
            
            if name and rating and feedback_text:
                Feedback.objects.create(
                    name=name,
                    rating=int(rating),
                    feedback=feedback_text,
                    user=request.user if request.user.is_authenticated else None
                )
                messages.success(request, 'Thank you for your feedback!')
            else:
                messages.error(request, 'Please fill all feedback fields.')
        
        return redirect('contact')
    
    all_feedback = Feedback.objects.all().order_by('-created_at')[:10]
    return render(request, 'bakery/contact.html', {'feedbacks': all_feedback})

def cart(request):
    return render(request, 'bakery/cart.html')

def checkout(request):
    if request.method == 'POST':
        try:
            customer_name = request.POST.get('customer_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            zip_code = request.POST.get('zip_code')
            cart_items = request.POST.get('cart_items', '{}')
            total_amount = request.POST.get('total_amount', 0)
            
            if isinstance(total_amount, str):
                total_amount = Decimal(total_amount)
            
            order = CartOrder.objects.create(
                user=request.user if request.user.is_authenticated else None,
                customer_name=customer_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                zip_code=zip_code,
                items_json=cart_items,
                total_amount=total_amount,
                status='pending'
            )
            
            messages.success(request, f'Order #{order.id} placed successfully! Thank you for your purchase.')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error placing order: {str(e)}')
            return redirect('cart')
    
    return render(request, 'bakery/checkout.html')

def special_order(request):
    if request.method == 'POST':
        form = SpecialOrderForm(request.POST)
        if form.is_valid():
            special_order = form.save()
            messages.success(request, 'Your special order request has been submitted! We will contact you within 24 hours.')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SpecialOrderForm()
    
    return render(request, 'bakery/special_order.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')
    return render(request, 'bakery/registration/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not username or not password1 or not password2:
            messages.error(request, 'Please fill all fields.')
            return redirect('signup')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return redirect('signup')
        
        try:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome {username}!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('signup')
    
    return render(request, 'bakery/registration/signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    orders = CartOrder.objects.filter(user=user).order_by('-created_at')
    return render(request, 'bakery/profile.html', {'user': user, 'orders': orders})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'bakery/product_detail.html', {'product': product})

def order_confirmation(request, order_id):
    order = get_object_or_404(CartOrder, id=order_id)
    return render(request, 'bakery/order_confirmation.html', {'order': order})