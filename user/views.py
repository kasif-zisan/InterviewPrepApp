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
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

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
                '''login(request, user)
                return redirect('profile')
                return Response(request.user.id)'''
                access_token = create_access_token(user.id)
                refresh_token = create_refresh_token(user.id)
                response = Response()
                response.set_cookie(key = 'refreshToken', value = refresh_token, httponly = True)
                response.data = {
                    'token' : access_token
                }
                return response


class LogOut(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {
            'message' : 'you have been logged out'
        }
        #return redirect('home')
        return response


class Profile(APIView):
    def get(self, request):
        '''name = request.user.username
        
        return Response({'identification': name})'''
        auth = get_authorization_header(request).split()
        #return Response(auth)
        if auth and len(auth)==2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = User.objects.filter(pk = id).first()
            return Response(UserSerializer(user).data)
        
        raise AuthenticationFailed('unauthenticated from views')

class RefreshApiView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({'token' : access_token})

class About(APIView):
    def get(self, request):
        return Response()


