from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from user.models import Tag, Post, Comments
from .forms import SignUpForm, LoginForm
from .models import Post

def home(request):
    posts_all = Post.objects.all()
    return render(request, 'user/home.html', {'posts_all':posts_all})


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


def new_post(request):
    if request.method == "POST":
        post = Post()
        post.title = request.POST["title"]
        post.text = request.POST["body"]
        post.bump = 0
        #post.save()
        #post.objects.create()
    return render(request, 'user/newpost.html')

def feed (request):
    posts = Post.objects.all()
    return render(request, 'user/feed.html', {'posts' : posts})