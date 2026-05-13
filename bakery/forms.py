from django import forms
from .models import ContactMessage, Feedback, SpecialOrder, CartOrder

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'feedback', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your Feedback'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }

class SpecialOrderForm(forms.ModelForm):
    class Meta:
        model = SpecialOrder
        fields = ['name', 'email', 'phone', 'delivery_option', 'address', 'city', 'zip_code', 'items_requested', 'special_requests', 'preferred_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'delivery_option': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'items_requested': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your custom order...'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any allergies or special requests?'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        delivery_option = cleaned_data.get('delivery_option')
        address = cleaned_data.get('address')
        city = cleaned_data.get('city')
        zip_code = cleaned_data.get('zip_code')
        
        if delivery_option == 'delivery':
            if not address:
                self.add_error('address', 'Address is required for delivery')
            if not city:
                self.add_error('city', 'City is required for delivery')
            if not zip_code:
                self.add_error('zip_code', 'Zip code is required for delivery')