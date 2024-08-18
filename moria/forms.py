from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
import uuid
from . models import *

class LoginForm(forms.Form):
    email_or_phone = forms.CharField(
        label=_('Email or Phone'),
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': _('Email or phone'),
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password'),
            'class': 'form-control'
        })
    )

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=255)

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password'),
            'class': 'form-control'
        })
    )
    confirm_password = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Confirm password'),
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_('Passwords do not match'))

        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('A user with this email already exists.'))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].split('@')[0]  # Use part of email before @ as username
        user.email = self.cleaned_data['email']

        # Ensure username is unique
        original_username = user.username
        counter = 1
        while User.objects.filter(username=user.username).exists():
            user.username = f"{original_username}{counter}"
            counter += 1

        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, email=self.cleaned_data['email'])
        return user
    
class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={
        'type': 'date'
    }))
    phone_number = forms.CharField(required=False)
    email = forms.EmailField()
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'phone_number']

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        # Update the email
        user.email = self.cleaned_data['email']
        
        # Update the password if it's provided
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
            profile.save()

        return profile