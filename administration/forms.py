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

class RegisterForm(forms.ModelForm):
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
    # Declaramos explícitamente los dos campos de contraseña
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'})
    )
    password2 = forms.CharField(
        label="Repetir Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita contraseña'})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "name", "surname")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Los dos campos de contraseña no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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

from django.forms import ModelForm, ValidationError
from landing.models import UserMessages

class UserMessageForm(ModelForm):
    class Meta:
        model = UserMessages
        fields = "__all__"