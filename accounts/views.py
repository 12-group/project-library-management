from unicodedata import name
from django.shortcuts import render, redirect 
from django.http import HttpResponse

def home(request):
   return render(request,'pages/home.html')

def search_book(request):
   return render(request,'pages/search.html')

def search_result_book(request):
   return render(request,'pages/search_result.html')

def detail_info_book(request):
   return render(request,'pages/book_detail.html')

def login(request):
   return render(request,'pages/login.html')

def register(request):
   return render(request,'pages/register.html')
