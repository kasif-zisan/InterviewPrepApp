from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login
# Create your views here.
def firstPage(request):
    if request.method=="GET":
        return render(request, 'user/firstPage.html', {'form' : UserCreationForm()})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                new_user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                new_user.save()
                login(request, new_user)
                return redirect('profile')
        except IntegrityError:
             return render(request, 'user/firstPage.html', {'form' : UserCreationForm(), 'error': "This username is already taken. Please try a new username."})

        else:
            return render(request, 'user/firstPage.html', {'form' : UserCreationForm(), 'error': "Passwords did not match. Please input the passwords correctly."})
def profile(request):
    return render(request, 'user/profile.html')
