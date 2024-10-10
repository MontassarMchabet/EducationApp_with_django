from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
class LoginForm(forms.Form):
   username = forms.CharField(label="Nom d'utilisateur")
   password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")