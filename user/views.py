from audioop import add
from cmath import log
from hashlib import new
from pickle import NONE
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from user.models import Tag, Post, Comments
from .forms import SignUpForm, LoginForm
from .models import Post
import os

def verify(request, user, address):
    print("vai kaaz kor")
    code = str(os.urandom(8))
    email = EmailMessage("Activation Code", "Your activation code is " + code, to = [address])
    email.send()
    check = request.POST.get('check', NONE)
    if check == code:
        user.save()
        login(request, user)
        return redirect('profile')
    return render(request, 'user/verify.html')

def home(request):
    return render(request, 'user/home.html')


def signUp(request):
    if request.method=="GET":
        return render(request, 'user/signUp.html', {'form' : SignUpForm()})
    else:
        print(request.POST['password1'])
        print(request.POST['password2'])
        try:
            if request.POST['password1'] == request.POST['password2'] or request.POST['password1'] != request.POST['password2']:
                new_user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                #new_user.save()
                #login(request, new_user)
                #verify(request, new_user, new_user.email)
                return redirect('user:verify', new_user, new_user.email)
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

def postdetails(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    return render(request, 'user/details.html', {'post' : post})