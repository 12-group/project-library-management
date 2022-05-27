from unicodedata import name
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .decorators import *

def register(request):

   form = CreateUserForm()
   if request.method == 'POST':
      form = CreateUserForm(request.POST)
      if form.is_valid():
         user = form.save()
         username = form.cleaned_data.get('username')

         messages.success(request, 'Đã tạo tài khoản cho ' + username)

         return redirect('login')
      
   context = {'form':form}
   return render(request, 'pages/register.html', context)

def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'pages/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home')
   
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'pages/account_setting.html', context)

def home(request):
   return render(request,'pages/home.html')

def search_book(request):
   return render(request,'pages/search.html')

def search_result_book(request):
   return render(request,'pages/search_result.html')

def detail_info_book(request):
   return render(request,'pages/book_detail.html')
