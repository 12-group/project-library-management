from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import IntegrityError

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

            if group == None:
                raise ValueError('Chưa có group reader')

            user.groups.add(group)

            messages.success(request, 'Tạo tài khoản thành công.')
            return redirect('login')

    context = {'form':form}
    return render(request, 'pages/user_account/register.html', context)

@unauthenticated_user
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
            if user.groups.filter(name='staff').exists():
                if user.customer.staff.force_password_change:
                    return redirect('password_change')
            return redirect('home')

        else: 
            messages.info(request, 'Tên đăng nhập hoặc mật khẩu chưa đúng.')
            
    context = {}
    return render(request, 'pages/user_account/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
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


@login_required(login_url='login')
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

@login_required(login_url='login')
def password_change_done(request):
    context = {}
    return render(request, 'pages/user_account/password_change_done.html', context)

def get_username(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return username

# @login_required(login_url='login')
# @admin_only
def home(request):
    books = Book.objects.all()
    if len(books) >= 4:
        top_book = books[:4]
        print(top_book)
        return render(request,'pages/home.html',{'books':books,'top_book':top_book})
    return render(request,'pages/home.html',{'books':books,'top_book':books})

def search_book(request):
    books = Book.objects.all()
    num_books = len(books)
    return render(request,'pages/reader/search.html',{'books':books,'num_books':num_books})

#kiểm tra sách này đã có trong giỏ hàng của độc giả chưa
def get_Cart_from_Reader_and_book(reader,book):
    try:
        return Cart.objects.get(reader = reader, book = book)
    except Cart.DoesNotExist:
        return None
#kiểm tra sách này đã có trong danh sách đã mượn của độc giả chưa
def get_Borrow_from_Reader_and_book(reader,book):
    try:
        return BorrowBook.objects.get(reader = reader, book = book)
    except BorrowBook.DoesNotExist:
        return None



def detail_info_book(request,pk):
    book = Book.objects.get(bId=pk)
    user = User.objects.get(username =get_username(request) )
    reader = Reader.objects.get(user=user)

    if request.method == 'POST':
        if get_Cart_from_Reader_and_book(reader,book) is None:
            cart = Cart()
            cart.reader = reader
            cart.book = book 
            cart.save()
        elif get_Borrow_from_Reader_and_book (reader,book) is not None:
            raise ValueError('Bạn đã mượn sách này trước đó.')
        else:
            raise ValueError('Đã có trong giỏ hàng')
    return render(request,'pages/reader/book_detail.html',{'book':book})
   
def cart(request):
    user = User.objects.get(username =get_username(request) )
    reader = Reader.objects.get(user=user)
    cart = Cart.objects.filter(reader = reader)
    count_book = len(cart)
    if request.method == 'POST': #đăng ký mượn 
        #xóa toàn bộ sách trong giỏ hàng
        order = BorrowOrder()
        order.reader = reader
        print(reader.rId)
        for book in cart:
            print(book.book.bId)
            # giảm số lượng sách 
            b = Book.objects.get(bId = book.book.bId)
            b.number_of_book_remain -= 1
            b.save()
            #thêm thông tin order
            print(book.book)
            order.list_book.append(book.book)
            print(order.list_book)
            order.save()
            print("xong")
        cart.delete()
        count_book = len(cart)

    context = {
        'books':cart,
        'count_book':count_book
        }
    return render(request,'pages/reader/cart.html',context)
def order_book(request,pk):
    reader = Reader.objects.get(rId=pk)
    print(reader.rId)
    order = BorrowOrder.objects.get(reader = reader)
    print(order.list_book)
    return render(request,'pages/librarian/request_online.html',{'order':order})


def reader_borrow_detail(request):
    user = User.objects.get(username =get_username(request) )
    reader = Reader.objects.get(user=user)
    borrowBook = BorrowBook.objects.filter(reader = reader)

    return render(request,'pages/reader/reader_borrow_detail.html',{'borrowBook':borrowBook})

#--THỦ THƯ
def librarian_home(request):
    readers = Reader.objects.all()
    context = {'readers':readers}
    return render(request,'pages/librarian/reader_list.html',context)

def borrowers(request):
    context = {}
    return render(request,'pages/librarian/borrower_list.html',context)


def get_object(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

@login_required(login_url='login')
def register_reader(request):
    form = ReaderForm()
    if request.method == 'POST':
        form = ReaderForm(request.POST)

        username = request.POST.get("username", "")

        user = User.objects.filter(username=username).exists()

        if not user:
            messages.error(request, 'Độc giả chưa có tài khoản.')
            return redirect('register_reader')
        else:
            user = User.objects.get(username=username)

        if form.is_valid():

            
            reader = form.save()
            reader.user = user
            reader.card_maker = request.user.customer.staff
            try:
                reader.save()
            except IntegrityError:
                messages.error(request, 'Đã có độc giả/nhân viên khác sử dụng tài khoản "' + user.username + '"')
                reader.delete()
                return redirect('register_reader')

            messages.success(request, 'Thêm độc giả thành công.')
            return redirect('librarian')

    return render(request,'pages/librarian/register_reader.html',{'form':form})

def request_onl_list(request):
    orders = BorrowOrder.objects.all()
    context={'orders':orders}
    return render(request,'pages/librarian/request_onl_list.html',context)

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
    ticket = PenaltyTicket.objects.get(id=pk)
    return render(request,'pages/librarian/penalty_ticket.html',{'ticket':ticket})

#---THỦ KHO
def list_book(request):
    books = Book.objects.all()
    count_books = books.count()
    context = {
        'books':books,
        'count_books':count_books
    }
    return render(request,'pages/stockkeeper/list_book.html',context)
    
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
                DEFAULT_PASSWORD
            )
            staff = staff_form.save()
            staff.user = user
            staff.save()
    
            staff_group = Group.objects.get(name='staff')
            user.groups.add(staff_group)

            if staff.position != 'Staff':
                staff.service = 'Manager deparment'
                staff.save()
                manager_group = Group.objects.get(name='manager')
                user.groups.add(manager_group)
            else:
                not_manager_group = Group.objects.get(name=staff.service.lower())
                user.groups.add(not_manager_group)

            messages.success(
                request,
                'Thêm nhân viên thành công.\n'
                'Tên tài khoản = {} \n'
                'Mật khẩu mặc định = {} '.format(user.username, DEFAULT_PASSWORD)
                )
            return redirect('manager_dashboard')

    context = {
        'form':staff_form,
        'user_form':user_form
        }
    return render(request, 'pages/manager/register_staff.html', context)

def delete_staff(request, sId):
    staff = Staff.objects.get(sId=sId)

    if request.method == 'POST':
        name = staff.name

        user = staff.user
        user.delete()

        messages.success(request, 'Xóa nhân viên {} thanh cong'.format(name))
        return redirect('manager_dashboard')

    context={
        'staff':staff
    }

    return render(request, 'pages/manager/delete_staff.html', context)
