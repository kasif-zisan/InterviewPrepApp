from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .forms import SignUpForm, LoginForm
# Create your views here.
def home(request):
    return render(request, 'user/home.html')
def signUp(request):
    if request.method=="GET":
        return render(request, 'user/signUp.html', {'form' : SignUpForm()})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                new_user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                new_user.save()
                login(request, new_user)
                return redirect('profile')
        except IntegrityError:
             return render(request, 'user/signUp.html', {'form' : SignUpForm(), 'error': "This username is already taken. Please try a new username."})

        else:
            return render(request, 'user/signUp.html', {'form' : SignUpForm(), 'error': "Passwords did not match. Please input the passwords correctly."})
def logIn(request):
    if request.method=="GET":
        return render(request, 'user/login.html', {'form' : LoginForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'user/login.html', {'form' : LoginForm(), 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('profile')
def logOut(request):
    logout(request)
    return redirect('home')
def profile(request):
    return render(request, 'user/profile.html')
def about(request):
    return render(request, 'user/about.html')
