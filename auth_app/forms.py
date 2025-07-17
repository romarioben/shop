from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django import forms
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()



class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ': 'true', 
    'class':'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label= 'Mot de passe', 
    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label= 'Confirmer Mot de passe', 
    widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ': 'true', 
    'class':'form-control'}))
    password = forms.CharField(label= 'Password', 
    widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))



class PassWordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Ancien password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, 'class':'form-control'}
        ),
    )
    new_password1 = forms.CharField(
        label="Nouveau Password 1",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, 'class':'form-control'}
        ),
    )
    new_password2 = forms.CharField(
        label="Nouveau password 2",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, 'class':'form-control'}
        ),
    )

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget = forms.PasswordInput(attrs=
    {'autocomplete':'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput(attrs=
    {'autocomplete':'current-password', 'class':'form-control'}))
