from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "mobile_number", "date_of_birth", "user_gender", "position_status")
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date input
        }
