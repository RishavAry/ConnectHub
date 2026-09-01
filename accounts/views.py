from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm
# from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
            )
            return redirect('login')

        else:
            form = RegisterForm()

        return render(request, 'accounts/register.html', {'form': form})


    return render(request, 'accounts/register.html')

