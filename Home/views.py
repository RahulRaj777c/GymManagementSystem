from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from gymmanagement.Startup.models import TrainerProfile
from .models import trainer
# Create your views here.

def index (request):
  
     return render(request,'index.html')
  
def about(request):
     return render(request,'about.html')
def trainners(request):
    dict_tr={
        'train':TrainerProfile.objects.all()
    }
    return render(request,'trainers.html',dict_tr)
def membership(request):
      return render(request,'membership.html')
def contact(request):
      return render(request,'contact.html')
def loginn(request):
      return render(request,'login.html') #login

def signupp(request):
      from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def signupp(request):
    '''if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if username and email and password:
            try:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "User registered successfully")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect('signup')
        else:
            messages.error(request, "Please fill all fields")
            return redirect('login')'''
    return render(request,'signup.html') #signup
