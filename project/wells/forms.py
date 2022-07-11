from django import forms 

class Auth_form(forms.Form):
    login = forms.CharField(widget = forms.TextInput)
    password = forms.CharField(widget = forms.PasswordInput)