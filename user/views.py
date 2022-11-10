
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .models import Post, Comments, Profile
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, StringSerializer, EditPostSerializer, LogInSerializer, SignUpSerializer
import random

class Home(APIView):
    def get(self, request):
        return Response()

def verify(request):
    username = request.session['username']
    password = request.session['password']
    email = request.session['email']
    if request.method == "GET":
        verification_code = str(random.randrange(1000,9999))
        request.session['verification_code'] = verification_code
        send_code = EmailMessage("Activation Code", "Your activation code is " + verification_code, to=[email])
        send_code.send()
        return render(request, 'user/verify.html')
    else:
        code = request.session['verification_code']
        if request.POST['check'] == code:
            new_user = User.objects.create_user(username, password = password)
            new_user.save()
            profile = Profile.objects.create(works_at = request.POST['works_at'], user = new_user)
            profile.save()
            login(request, new_user)
            return redirect('profile')
    return render(request, 'user/verify.html')


class Verify(APIView):
    def get(self, request):
        self.__sendVerificationCode()
        return Response()

    def post(self, request):
        codeSerializer = StringSerializer(data=request.data)
        if codeSerializer.is_valid():
            code = codeSerializer.validated_data['text']
            verificationCode = request.session['verification_code']
            if code == verificationCode:
                username = request.session['username']
                name = request.session['name']
                email = request.session['email']
                worksAt = request.session['worksAt']
                password = request.session['password']

                new_user = User.objects.create_user(username, password=password, email=email)
                new_user.save()

                profile = Profile.objects.create(works_at=worksAt, name=name, user=new_user)
                profile.save()
                
                return redirect('profile')
            else:
                return Response({"error": "aam patay pudina, tore ami chudina"})
            

    def __sendVerificationCode(self, request):
        verification_code = str(random.randrange(1000,9999))
        request.session['verification_code'] = verification_code
        send_code = EmailMessage("Activation Code", "Your activation code is " + verification_code, to=[email])
        send_code.send()


class SignUp(APIView):
    def get(self, request):
        return Response()
    
    def post(self, request):
        signupInfo = SignUpSerializer(data=request.data)
        if signupInfo.is_valid():
            try:
                username = signupInfo.validated_data['username']
                name = signupInfo.validated_data['name']
                email = signupInfo.validated_data['email']
                worksAt = signupInfo.validated_data['worksAt']
                password = signupInfo.validated_data['password']
                passwordConfirm = signupInfo.validated_data['passwordConfirm']
                if password == passwordConfirm:
                    request.session['username'] = username
                    request.session['name'] = name
                    request.session['email'] = email
                    request.session['worksAt'] = worksAt
                    request.session['password'] = password
                    return redirect('verify')
            except IntegrityError:
                return Response({"error": "get a better name loser"})
            else:
                return Response({"error": "bro your password is shit"})


class LogIn(APIView):
    def get(self, request):
        return Response()
    
    def post(self, request):
        loginInfo = LogInSerializer(data=request.data)
        if loginInfo.is_valid():
            user = authenticate(
                request, 
                username = loginInfo.validated_data['username'], 
                password = loginInfo.validated_data['password']
            )
            if user is None:
                return Response({'error': "Username and password did not match"})
            else:
                login(request, user)
                return redirect('profile')


class LogOut(APIView):
    def get(self, request):
        logout(request)
        return redirect('home')


class Profile(APIView):
    def get(self, request):
        return Response()


class About(APIView):
    def get(self, request):
        return Response()


class NewPost(APIView):
    def get(self, request):
        return Response()
    
    def post(self, request):
        temp = EditPostSerializer(data=request.data)
        if temp.is_valid():
            post_title = temp.validated_data['title']
            post_text = temp.validated_data['text']
            new_post = Post.objects.create(title=post_title, text = post_text, bump = 0, author = request.user)
            new_post.save()
        return redirect('feed')


class PostAll(ListAPIView):
    def get_queryset(self):
        return Post.objects.all()
    def get_serializer_class(self):
        return PostSerializer


class PostDetails(APIView):
    def get(self, request, post_id):
        self.__show(post_id)
    
    def post(self, request, post_id):
        postObj = get_object_or_404(Post, pk=post_id)
        newCommentSerializer = StringSerializer(data=request.data)
        if newCommentSerializer.is_valid():
            comment_text = newCommentSerializer.validated_data['text']
            new_comment = Comments.objects.create(text=comment_text, bump=0, author=request.user, parent=postObj)
            new_comment.save()
        else:
            print('i dont know what went wrong tbh')
        
        self.__show(post_id)
    
    def put(self, request, post_id):
        editPostSerializer = EditPostSerializer(data=request.data)
        if editPostSerializer.is_valid():
            post_title = editPostSerializer.validated_data['title']
            post_text = editPostSerializer.validated_data['text']
            if not post_title or post_title == '':
                Post.objects.filter(pk = post_id).update(text = post_text)
            elif not post_text or post_text == '':
                Post.objects.filter(pk = post_id).update(title = post_title)
            else:
                Post.objects.filter(pk = post_id).update(title=post_title, text = post_text)
        self.__show(post_id)
        
    def __show(self, id):
        postObj = get_object_or_404(Post, pk=id)
        postSerializer = PostSerializer(postObj)
        commentsObjAll = Comments.objects.filter(parent=id)
        commentsSerializerAll = CommentSerializer(commentsObjAll, many=True)
        return Response({'post': postSerializer.data, 'comments': commentsSerializerAll.data})