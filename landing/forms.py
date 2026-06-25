from django import forms
from .models import UserMessages

class ContactForm(forms.ModelForm):
    class Meta:
        model = UserMessages
        fields = ['name', 'surname', 'email', 'phone', 'message']