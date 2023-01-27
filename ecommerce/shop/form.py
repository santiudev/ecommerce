from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import User

from django import forms


#Register Form


class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba su usario'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba su correo electronico'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Crea su contraseña'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirme su contraseña'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']


#Password Changing Form


class PasswordChangingForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña vieja'}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Crea su nueva contraseña'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirme su contraseña'}))
    class Meta:
        model=User
        fields=['old_password','new_password1','new_password2']


