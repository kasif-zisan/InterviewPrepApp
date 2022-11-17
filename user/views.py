from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .models import UserProfile
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import UserSerializer, StringSerializer, LogInSerializer, SignUpSerializer
import random

class Home(APIView):
    def get(self, request):
        print(request.user)
        return Response({"Zarcode": "It is the platform for interview preparation in Bangladesh"})


class Verify(APIView):
    def get(self, request):
        verification_code = str(random.randrange(1000,9999))
        request.session['verification_code'] = verification_code
        email = request.session['email']
        send_code = EmailMessage("Activation Code", "Your activation code is " + verification_code, to=[email])
        send_code.send()
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

                profile = UserProfile.objects.create(works_at=worksAt, name=name, user=new_user)
                profile.save()
                
                return redirect('profile')
            else:
                return Response({"error": "your email is not verified. Please try again."})


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
                return Response({"error": "This username is already taken"})
            else:
                return Response({"error": "Username and Password did not match"})


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


