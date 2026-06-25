from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from administration.models import CustomUser

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@ejemplo.com',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-control'
        })
    )

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    surname = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'})
    )
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@ejemplo.com',
            'class': 'form-control'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("name", "surname", "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password1' in self.fields:
            self.fields['password1'].label = "Contraseña"
            self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})
        if 'password2' in self.fields:
            self.fields['password2'].label = "Repetir Contraseña"
            self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita contraseña'})


class RecoveryForm(forms.Form):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@ejemplo.com',
            'class': 'form-control'
        })
    )

class VerificationForm(forms.Form):
    code = forms.CharField(
        label="Codigo",
        widget=forms.EmailInput(attrs={
            'placeholder': '',
            'class': 'form-control'
        })
    )

# forms.py

from django.forms import ModelForm
from landing.models import UserMessages

class UserMessageForm(ModelForm):
    class Meta:
        model = UserMessages
        fields = "__all__"