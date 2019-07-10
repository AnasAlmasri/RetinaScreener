from django import forms

class RegistrationForm(forms.Form):
    f_name = forms.CharField()
    l_name = forms.CharField()
    email = forms.EmailField()
    password = forms.PasswordInput()