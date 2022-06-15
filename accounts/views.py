from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import IntegrityError

from .models import *
from .forms import *
from .decorators import *
from .filter import *

from .initial_func import username_gen

from datetime import date
import json

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
            messages.error(request, 'Tên đăng nhập không được để trống')

        elif password == '' : 
            messages.error(request, 'Mật khẩu không được bỏ trống')

        elif user is not None:
            login(request, user)
            if user.groups.filter(name='staff').exists():
                if user.customer.staff.force_password_change:
                    return redirect('password_change')
            return redirect('home')

        else: 
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu chưa đúng.')
            
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
            if user.groups.filter(name='staff').exists():
                if user.customer.staff.force_password_change:
                    staff = user.customer.staff
                    staff.force_password_change = False
                    staff.save()
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
    print(request.GET)
    books_filter = BookFilter(request.GET, queryset=books)
    books = books_filter.qs
    print(books)
    num_books = len(books)

    context = {
        'books':books,
        'num_books':num_books,
        'books_filter':books_filter
    }
    return render(request,'pages/reader/search.html',context)

def detail_info_book(request,pk):
    book = Book.objects.get(bId=pk)
    user = User.objects.get(username =get_username(request) )
    
    is_reader = Reader.objects.filter(user=user).exists()
    if request.method == 'POST':
        if is_reader is False:
            messages.error(request,'Độc giả mới có quyền đăng ký mượn sách')
            return render(request,'pages/reader/book_detail.html',{'book':book})
        elif book.number_of_book_remain <=0 :
            messages.error(request,'Sách đã được mượn hết')
            return render(request,'pages/reader/book_detail.html',{'book':book})

        else:
            reader = Reader.objects.get(user=user)
            if Cart.objects.filter(reader = reader).exists() is False:
                cart = Cart()
                cart.reader = reader
                cart.book = book 
                cart.save()
                messages.success(request,'Thêm {} vào giỏ hàng thành công'.format(book.name))
            elif Cart.objects.filter(reader = reader).exists() is True:
                messages.error(request,'Sách đã có trong giỏ hàng')
                return render(request,'pages/reader/book_detail.html',{'book':book})

            elif BorrowOrder.objects.filter(reader = reader).exists() is True:
                borrow = BorrowOrder.objects.get(reader = reader)
                if book in borrow.list_book:
                    messages.error(request,'Bạn đã mượn sách này trước đó')
                    return render(request,'pages/reader/book_detail.html',{'book':book})
    return render(request,'pages/reader/book_detail.html',{'book':book})
   
def cart(request):
    user = User.objects.get(username =get_username(request) )
    reader = Reader.objects.get(user=user)
    cart = Cart.objects.filter(reader = reader)

    count_book = len(cart)
    order = BorrowOrder()
    order.reader = reader
    test_string = '{}' 
    order.list_book = json.loads(test_string)

    print(type(order.list_book))

    if request.method == 'POST': #đăng ký mượn 
        #xóa toàn bộ sách trong giỏ hàng
        for book in cart:
            # giảm số lượng sách 
            b = Book.objects.get(bId = book.book.bId)
            b.number_of_book_remain -= 1
            b.save()
            #thêm thông tin order
            #--thêm kiểm tra đã có 1 order khác chưa
            # print('{}'.format(book.book.bId))
            # print('{}'.format(book.book.bId))
            # print(type(order.list_book))
            # print(type(order)
            print(type(order.list_book))
            order.list_book['{}'.format(book.book.bId)] = '{}'.format(book.book.name)
            print(order.list_book)

            order.save()

        cart.delete()
        count_book = len(cart)

    context = {
        'cart':cart,
        'count_book':count_book
        }
    return render(request,'pages/reader/cart.html',context)

def remove_from_cart(request, cart_pk):
    cart = Cart.objects.get(pk=cart_pk)

    if request.method == 'POST':
        book_name = cart.book.name
        cart.delete()
        messages.success(request,'Lấy {} khỏi giỏ hàng thành công'.format(book_name))
        return redirect('cart')

    context = {
        'cart':cart
    }
    return render(request,'pages/reader/remove_from_cart.html',context)

def reader_borrow_detail(request):
    user = User.objects.get(username =get_username(request) )
    reader = Reader.objects.get(user=user)
    borrow = BorrowBook.objects.get(reader = reader)
    list =  zip(borrow.list_book,borrow.list_book.values())
    context = {'borrow':borrow,'list':list}
    return render(request,'pages/reader/reader_borrow_detail.html',context)

#--THỦ THƯ
def librarian_home(request):
    readers = Reader.objects.all()
    context = {'readers':readers}
    return render(request,'pages/librarian/reader_list.html',context)

def borrowers(request):
    borrows = BorrowBook.objects.all()
    context = {'borrows':borrows}
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

def request_onl(request,pk):
    order = BorrowOrder.objects.get(id=pk)
    list =  zip(order.list_book,order.list_book.values())
    if request.method == 'POST':
        order.status = 'Đang soạn sách'
        order.save()
        return redirect('request_onl_list')
    return render(request,'pages/librarian/request_online.html',{'order':order,'list':list})

def update_request(request,pk):
    order = BorrowOrder.objects.get(id=pk)
    form = OrderForm(instance=order)    
    list = []
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            if order.status == 'Đã nhận sách':
                borrow = BorrowBook()
                borrow.reader = order.reader
                borrow.list_book = order.list_book
                list =  zip(borrow.list_book,borrow.list_book.values())
                borrow.save()
                order.list_book.clear()
            return redirect('request_onl_list')
    context = {'form':form,'list':list}
    return render(request, 'pages/librarian/update_status_request.html', context)

def request_off(request):
    readers = Reader.objects.all()
    books = Book.objects.all()
    context = {'readers': readers,
                'books': books}
    return render(request,'pages/librarian/request_offline.html')
def borrow_detail(request,pk):
    borrow = BorrowBook.objects.get(id=pk)
    list =  zip(borrow.list_book,borrow.list_book.values())
    context = {'borrow':borrow,'list':list}
    return render(request,'pages/librarian/borrow_detail.html',context)

def return_book(request,pk):
    return_book = ReturnBook.objects.get(id=pk)
    list =  zip(return_book.list_book,return_book.list_book.values())
    context = {'return_book': return_book,'list':list}
    return render(request,'pages/librarian/return_book.html', context)

def penalty_ticket(request,pk):
    ticket = PenaltyTicket.objects.get(id=pk)
    return render(request,'pages/librarian/home.html',{'ticket':ticket})

#---THỦ KHO
def list_book(request):
    books = Book.objects.all()
    count_books = books.count()
    context = {
        'books':books,
        'count_books':count_books
    }
    return render(request,'pages/stockkeeper/list_book.html',context)

# re-confirm liquidation screen
def thanh_ly(request):
    today = date.today()
    if request.method == 'POST':
        book_liquidation_form = BookLiquidationForm(request.POST)
        print(request.POST)
        action = request.POST.get('submit')
        if action == 'reconfirm':
            pass
        elif action == 'confirm':
            book_liquidation_form.save()
            messages.success(request,'Thanh lý thành công')
            return redirect('list_book')

    context = {
        'user': request.user,
        'date': today.strftime("%d/%m/%Y"),
        'form': book_liquidation_form
    }
    return render(request,'pages/stockkeeper/thanh_ly.html', context)

# fill in liquidation info screen
def liquidation_info(request, bId):

    book = Book.objects.get(bId=bId)
    book_liquidation_form = BookLiquidationForm(
        initial={
            'staff':request.user.customer.staff,
            'book':book
        }
    )
    book_liquidation_form.fields['staff'].widget = forms.HiddenInput()
    book_liquidation_form.fields['book'].widget = forms.HiddenInput()

    context={
        'form':book_liquidation_form,
        'book':book
    }

    return render(request,'pages/stockkeeper/liquidation_info.html', context)

def liquidation_history(request):
    liquidation = BookLiquidation.objects.all()
    context = {
        'liquidation':liquidation,
    }
    return render(request,'pages/stockkeeper/liquidation_history.html',context)

def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            book.nguoinhan = request.user.customer.staff
            book.number_of_book_remain = book.total
            book.save()
            messages.success(request, "Sách được thêm thành công với ID là " + book.bId)
            return redirect('list_book')
        
    context = {'form':form}
    return render(request, 'pages/stockkeeper/add_book.html', context)

#--THỦ QUỸ
def receipt_list(request):
    return render(request,'pages/cashier/receipt_list.html')

def add_receipt(request):
    return render(request,'pages/cashier/add_receipt.html')

#--QUẢN LÝ
def manager_dashboard(request):
    staffs = Staff.objects.all()
    staff_filter = StaffFilter(request.GET, queryset=Staff.objects.all())
    staffs = staff_filter.qs

    context = {
        'staffs':staffs,
        'staff_filter': staff_filter
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
                staff.service = 'Manager department'
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
