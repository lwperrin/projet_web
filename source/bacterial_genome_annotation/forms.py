#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class UserCreationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.EmailField()
    class Meta:
        model = User
        fields = ['email','password']


class UserChangeForm(forms.Form):
    
    class Meta:
        model = User
        fields = ('email',)