from cgitb import text
import email
import random
from turtle import title, update
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from django.views.generic import CreateView
from .forms import SignUpForm, LoginForm, PostForm
from .models import Post, Comments, Profile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, jsonString, postString
import datetime


def home(request):
    return render(request, 'user/home.html')
#commenting this out just to avoid email verification
'''def verify(request):
    username = request.session['username']
    password = request.session['password']
    email = request.session['email']
    #print(username)
    #print(password)
    #print(email)
    if request.method == "GET":
        verification_code = str(random.randrange(1000,9999))
        request.session['verification_code'] = verification_code
        send_code = EmailMessage("Activation Code", "Your activation code is " + verification_code, to=[email])
        send_code.send()
        return render(request, 'user/verify.html')
    else:
        code = request.session['verification_code']
        #print(code)
        if request.POST['check'] == code:
            new_user = User.objects.create_user(username, password = password)
            new_user.save()
            login(request, new_user)
            return redirect('profile')
    return render(request, 'user/verify.html')

def signUp(request):
    if request.method=="GET":
        return render(request, 'user/signUp.html', {'form' : SignUpForm()})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                username = request.POST['username']
                password = request.POST['password1']
                email = request.POST['email']
                request.session['username'] = username
                request.session['password'] = password
                request.session['email'] = email
                #new_user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                #new_user.save()
                #login(request, new_user)
                #verify(request, new_user, new_user.email)
                return redirect('verify')
        except IntegrityError:
             return render(request, 'user/signUp.html', {'form' : SignUpForm(), 'error': "This username is already taken. Please try a new username."})
        else:
            return render(request, 'user/signUp.html', {'form' : SignUpForm(), 'error': "Passwords did not match. Please input the passwords correctly."})

'''
def signUp(request):
    if request.method=="GET":
        return render(request, 'user/signUp.html', {'form' : SignUpForm()})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                new_user = User.objects.create_user(request.POST['username'], password = request.POST['password1'], email = request.POST['email'])
                new_user.save()
                profile = Profile.objects.create(works_at = request.POST['works_at'], user = new_user)
                profile.save()
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


'''def new_post(request):
    if request.method == "POST":
        post = Post()
        post.title = request.POST["title"]
        post.text = request.POST["body"]
        post.bump = 0
        #post.save()
        #post.objects.create()
    return render(request, 'user/newpost.html')'''

'''class new_post(CreateView):
    model = Post
    form_class = PostForm
    template_name= 'user/newpost.html'
    '''

@api_view(['GET', 'POST'])
def new_post(request):
    if request.method  == 'POST':
        temp = postString(data=request.data)
        if temp.is_valid():
            post_title = temp.validated_data['title']
            post_text = temp.validated_data['text']
            new_post = Post.objects.create(title=post_title, text = post_text, image = None, bump = 0, author = request.user)
            new_post.save()
        post = postString()
        return Response({'newpost': post.data})
    if request.method == 'GET':
        post = postString()
        return Response({'newpost': post.data})

    
@api_view()
def post_all(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    user = request.user
    return Response({'allposts': serializer.data, 'test': user.username})

@api_view(['GET', 'POST', 'PUT'])
def post_details(request, post_id):
    obj = get_object_or_404(Post, pk=post_id)
    post = PostSerializer(obj)
    if request.method == "GET":
        obj = Comments.objects.filter(parent=post_id)
        comments = CommentSerializer(obj, many=True)
        return Response({'post': post.data, 'comments': comments.data})
    if request.method == "POST":
        tmep = jsonString(data=request.data)
        if tmep.is_valid():
            comment_text = tmep.validated_data['text']
            new_comment = Comments.objects.create(text=comment_text, image=None, bump=0, author=request.user, parent=obj)
            new_comment.save()
        else:
            print("this is truly sad")
        obj = Comments.objects.filter(parent=post_id)
        comments = CommentSerializer(obj, many=True)
        return Response({'post': post.data, 'comments': comments.data})
    if request.method == "PUT":
        temp = postString(data=request.data)
        if temp.is_valid():
            post_title = temp.validated_data['title']
            post_text = temp.validated_data['text']
            Post.objects.filter(pk = post_id).update(title=post_title, text = post_text, bump = 0, author = request.user)
        obj = Comments.objects.filter(parent=post_id)
        comments = CommentSerializer(obj, many=True)
        postobj = get_object_or_404(Post, pk=post_id)
        postget = PostSerializer(postobj)
        return Response({'post': postget.data, 'comments': comments.data})