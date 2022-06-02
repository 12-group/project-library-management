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
            form.save()            
            messages.success(request, 'Tạo tài khoản thành công.')
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
			messages.info(request, 'Tên đăng nhập hoặc mật khẩu chưa đúng.')

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
   
def cart(request):
   return render(request,'pages/cart.html')

#--THỦ THƯ
def librarian_home(request):
	return render(request,'pages/reader_list.html')
def borrowers(request):
	return render(request,'pages/borrower_list.html')
def register_reader(request):
	return render(request,'pages/register_reader.html')
def request_onl(request):
	return render(request,'pages/request_online.html')
def request_off(request):
	return render(request,'pages/request_offline.html')
def return_book(request):
	return render(request,'pages/return_book.html')
def phieu_phat(request):
	return render(request,'pages/phieuphat.html')

#---THỦ KHO
def list_book(request):
	return render(request,'pages/list_book.html')
def thanh_ly(request):
	return render(request,'pages/thanh_ly.html')
def add_book(request):
	form = BookForm()
	if request.method == 'POST':
	   form = BookForm(request.POST)
	   if form.is_valid():
	   	form.save()
	   	messages.success(request, "Sách được thêm thành công với ID là " + form.id)
	   	return redirect('add_book')
		
	context = {'form':form}
	return render(request, 'pages/add_book.html', context)