from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User, Profile


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        username = username.strip().lower()

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = email.strip().lower()

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")

        return email

    def clean_password(self):
        password = self.cleaned_data["password"]

        validate_password(password)

        return password

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    def clean (self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise ValidationError("Invalid username or password")
            cleaned_data["user"] = user

            return cleaned_data
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']