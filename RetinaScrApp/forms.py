from django import forms
from RetinaScrApp.models import Doctor

class RegistrationForm(forms.Form):
    f_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'f_name',
            'type': 'name',
            'class': 'form-control'
        }
    ))

    l_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'l_name',
            'type': 'name',
            'class': 'form-control'
        }
    ))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'id': 'email',
            'type': 'email',
            'class': 'form-control'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'id': 'password',
            'type': 'password',
            'class': 'form-control'
        }
    ))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'id': 'confirm_password',
            'type': 'password',
            'class': 'form-control'
        }
    ))


class LoginForm(forms.Form):
    login_email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'id': 'login_email',
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'Email'
        }
    ))

    login_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'id': 'login_password',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ))