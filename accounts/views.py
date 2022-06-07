from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .decorators import *

# @unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='reader')
            user.groups.add(group)
            Reader.objects.create(
                user=user,
                name=user.username,
                )
            messages.success(request, 'Tạo tài khoản thành công.')
            return redirect('login')

    context = {'form':form}
    return render(request, 'pages/register.html', context)

# @unauthenticated_user
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
    group = None
    form = None
    print(request.user.groups)
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'reader':
        reader = request.user.customer.reader
        form = ReaderForm(instance=reader)
    elif group == 'staff':
        staff = request.user.customer.staff
        form = StaffForm(instance=staff)

    if request.method == 'POST':
        if group == 'reader':
            form = ReaderForm(request.POST, request.FILES,instance=reader)
        elif group == 'staff':
            form = StaffForm(request.POST, request.FILES,instance=staff)

        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'pages/account_setting.html', context)



# @login_required(login_url='login')
# @admin_only
def home(request):
    books = Book.objects.all()
    if len(books) >= 4:
        top_book = books[len(books)-4:]
        top_book.reverse()
        return render(request,'pages/home.html',{'books':books,'top_book':top_book})
    return render(request,'pages/home.html',{'books':books,'top_book':books})

def search_book(request):
    return render(request,'pages/reader/search.html')
def search_result_book(request):
    books = Book.objects.all()
    num_books = len(books)
    return render(request,'pages/reader/search_result.html',{'books':books,'num_books':num_books})

def detail_info_book(request,pk):
    book = Book.objects.get(id=pk)	
    return render(request,'pages/reader/book_detail.html',{'book':book})
   
def cart(request):
   return render(request,'pages/reader/cart.html')

#--THỦ THƯ
def librarian_home(request):
    readers = Reader.objects.all()
    return render(request,'pages/librarian/reader_list.html',{'readers':readers})
def borrowers(request):
    return render(request,'pages/librarian/borrower_list.html')
def register_reader(request):
    return render(request,'pages/librarian/register_reader.html')
def request_onl(request):
    return render(request,'pages/librarian/request_online.html')
def request_off(request):
    return render(request,'pages/librarian/request_offline.html')
def return_book(request):
    return render(request,'pages/librarian/return_book.html')
def pernalty_ticket(request):
    return render(request,'pages/librarian/pernalty_ticket.html')

#---THỦ KHO
def list_book(request):
    books = Book.objects.all()
    count_books = books.count()
    return render(request,'pages/stockkeeper/list_book.html',{'books':books,'count_books':count_books})
def thanh_ly(request):
    return render(request,'pages/stockkeeper/thanh_ly.html')
def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sách được thêm thành công với ID là " + form.id)
            return redirect('add_book')
        
    context = {'form':form}
    return render(request, 'pages/stockkeeper/add_book.html', context)

#--THỦ QUỸ
def money_list(request):
    return render(request,'pages/cashier/money_list.html')

#--QUẢN LÝ
def manager_dashboard(request):
    staffs = Staff.objects.all()

    context = {
        'staffs':staffs
    }

    return render(request, 'pages/manager/manager_dashboard.html',context)