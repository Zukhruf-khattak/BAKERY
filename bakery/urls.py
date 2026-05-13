from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('special-order/', views.special_order, name='special_order'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),  # ADD THIS LINE
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]