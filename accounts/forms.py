from django import forms
from django.contrib.auth.forms import AuthenticationForm # 追加

from .models import User

class LoginFrom(AuthenticationForm):
    class Meta:
        model = User

from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'contact_address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_address': forms.TextInput(attrs={'class': 'form-control'}),
        }
