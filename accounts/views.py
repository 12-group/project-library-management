from csv import reader
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .decorators import *

from .initial_func import username_gen

def is_in_group(check_group, groups):
    if check_group in [group.name for group in groups]:
        return True
    return False

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
                email=user.email
                )
            messages.success(request, 'Tạo tài khoản thành công.')
            return redirect('login')

    context = {'form':form}
    return render(request, 'pages/user_account/register.html', context)

# @unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if username == '':
            messages.info(request, 'Tên đăng nhập không được để trống')
        elif password == '' : 
            messages.info(request, 'Mật khẩu không được bỏ trống')
        elif user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.info(request, 'Tên đăng nhập hoặc mật khẩu chưa đúng.')
            
    context = {}
    return render(request, 'pages/user_account/login.html', context)

# @login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

# @login_required(login_url='login')
def accountSettings(request):
    groups = None
    form = None
    
    if request.user.groups.exists():
        groups = request.user.groups.all()

    # if 'reader' in [group.name for group in groups]:
    if is_in_group('reader', groups):
        reader = request.user.customer.reader
        form = ReaderForm(instance=reader)

    # elif 'staff' in [group.name for group in groups]:
    elif is_in_group('staff', groups):
        staff = request.user.customer.staff
        form = StaffForm(instance=staff)

    if request.method == 'POST':
        # if 'reader' in [group.name for group in groups]:
        if is_in_group('reader', groups):
            form = ReaderForm(request.POST, request.FILES,instance=reader)

        # elif 'staff' in [group.name for group in groups]:
        if is_in_group('staff', groups):
            form = StaffForm(request.POST, request.FILES,instance=staff)

        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'pages/user_account/account_setting.html', context)


# @login_required(login_url='login')
def password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')

    context = {'form':form}
    return render(request, 'pages/user_account/password_change.html', context)

def password_change_done(request):
    context = {}
    return render(request, 'pages/user_account/password_change_done.html', context)


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
    books = Book.objects.all()
    return render(request,'pages/reader/cart.html',{'books':books})

#--THỦ THƯ
def librarian_home(request):
    readers = Reader.objects.all()
    context = {'readers':readers}
    return render(request,'pages/librarian/reader_list.html',context)

def borrowers(request):
    context = {}
    return render(request,'pages/librarian/borrower_list.html',context)

def get_username(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return username

def get_user_from_email(email):
    return User.objects.get(id=2)

def register_reader(request):
    form = ReaderForm()
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('email:',user.email,'')
            print(get_username(request))
            if user.email is not None:
                user_acc = User.objects.get(email = user.email)
            messages.success(request, 'Thêm độc giả thành công.')
            return redirect('librarian')
    return render(request,'pages/librarian/register_reader.html',{'form':form})

def request_onl(request):
    readers = Reader.objects.all()
    books = Book.objects.all()
    context = {'readers': readers,
                'books': books}
    return render(request,'pages/librarian/request_online.html',context)

def request_off(request):
    readers = Reader.objects.all()
    books = Book.objects.all()
    context = {'readers': readers,
                'books': books}
    return render(request,'pages/librarian/request_offline.html')

def return_book(request):
    return_books = ReturnBook.objects.all()
    context = {'return_books': return_books}
    return render(request,'pages/librarian/return_book.html', context)

def penalty_ticket(request,pk):
    ticket = FineReceipts.objects.get(id=pk)
    return render(request,'pages/librarian/penalty_ticket.html',{'ticket':ticket})

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

def add_staff(request):
    staff_form = StaffForm()
    user_form = CreateUserForm()

    if request.method == 'POST':
        staff_form = StaffForm(request.POST)
        if staff_form.is_valid():
            
            # print(username_gen())
            user = User.objects.create_user(
                username_gen(),
                '',
                'password'
            )
            

            
            staff = staff_form.save()
            staff.user = user
            staff.save()

            group = Group.objects.get(name='staff')
            user.groups.add(group)

            messages.success(request, 'Tạo tài khoản thành công.')
            return redirect('manager_dashboard')

    context = {
        'form':staff_form,
        'user_form':user_form
        }
    return render(request, 'pages/manager/register_staff.html', context)