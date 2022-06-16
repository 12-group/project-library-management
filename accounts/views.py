from re import S
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

@unauthenticated_user
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
                if user.groups.filter(name='librarian').exists():
                    return redirect('librarian')
                if user.groups.filter(name='stockkeeper').exists():
                    return redirect('list_book')
                if user.groups.filter(name='cashier').exists():
                    return redirect('receipt_list')
                if user.groups.filter(name='manager').exists():
                    return redirect('manager_dashboard')
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
            messages.success(request, 'Đổi mật khẩu thành công!')
            return redirect('password_change_done')

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

@login_required(login_url='login')
@redirect_home_view
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
            if Cart.objects.filter(reader = reader,book =book).exists() is True:
                print('y')
                messages.error(request,'Sách đã có trong giỏ hàng')
                return render(request,'pages/reader/book_detail.html',{'book':book})
            else:
                cart = Cart()
                cart.reader = reader
                cart.book = book 
                try:
                    cart.save()
                except Exception as e:
                    messages.error(request, e)
                    return render(request,'pages/reader/book_detail.html',{'book':book})
                messages.success(request,'Thêm {} vào giỏ hàng thành công'.format(book.name))
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
    context = {
    'cart':cart,
    'count_book':count_book
    }

    if request.method == 'POST': #đăng ký mượn 

        for book in cart:

            if BorrowOrder.objects.filter(reader = reader).exists() is True:
                borrow_order = BorrowOrder.objects.filter(reader = reader)
                for i in borrow_order:
                    if book.book.bId in i.list_book:
                        messages.error(request,'Bạn đã được đăng ký mượn {} trước đó'.format(book.book.name))
                        return render(request,'pages/reader/cart.html',context)

            elif BorrowBook.objects.filter(reader = reader).exists() is True:
                borrow = BorrowBook.objects.filter(reader = reader)
                for i in borrow:
                    if book.book.bId in i.list_book:
                        messages.error(request,'Bạn đã mượn {} trước đó'.format(book.book.name))
                        return render(request,'pages/reader/cart.html',context)

            order.list_book['{}'.format(book.book.bId)] = '{}'.format(book.book.name)
            try:
                order.save()
            except Exception as e:
                messages.error(request, e)
            redirect('cart')


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
    user = User.objects.get(username =get_username(request))
    reader = Reader.objects.get(user=user)
    borrow = BorrowBook()
    order = BorrowOrder()
    list_book_order= {}
    list_book_borrow= {}
    status_order = []
    date_borrow = []

    if BorrowOrder.objects.filter(reader = reader).exists() is True :
        order = BorrowOrder.objects.filter(reader = reader)
        for i in order:
            list_book_order.update(i.list_book)
            for j in i.list_book.values():
                status_order.append(i.status)
    if BorrowBook.objects.filter(reader = reader).exists() is True :
        borrow = BorrowBook.objects.filter(reader = reader)
        for i in borrow:     
            list_book_borrow.update(i.list_book)
            for j in i.list_book.values():
                date_borrow.append(i.date_borrow)

    list_order = zip(list_book_order,list_book_order.values(),status_order)
    list_borrow = zip(list_book_borrow,list_book_borrow.values(),date_borrow)

    context = {'list_order':list_order,'list_borrow':list_borrow}
    return render(request,'pages/reader/reader_borrow_detail.html',context)

#--THỦ THƯ
def librarian_home(request):
    readers = Reader.objects.all()
    context = {'readers':readers}
    return render(request,'pages/librarian/reader_list.html',context)

def borrowers(request):
    borrows = BorrowBook.objects.all()
    today = datetime.datetime.now()
    context = {
        'borrows':borrows,
        'today': today.strftime("%d/%m/%Y"),
        }
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


        if form.is_valid():
               
            try:
                reader = form.save()
            except Exception as e:
                messages.error(request, e)
                return redirect('register_reader')
            if user is True:
                user = User.objects.get(username=username)
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
        try:
            order.save()
        except Exception as e:
            messages.error(request, e)
            return render(request,'pages/librarian/request_online.html',{'order':order,'list':list})
        return redirect('request_onl_list')
    return render(request,'pages/librarian/request_online.html',{'order':order,'list':list})

def update_request(request,pk):
    order = BorrowOrder.objects.get(id=pk)
    form = OrderForm(instance=order)    
    list = []
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            try:
                form.save()
                context = {'form':form,'list':list}

                if order.status == 'Đã nhận sách':
                    #thêm vào ds mượn
                    if BorrowBook.objects.filter(reader = order.reader).exists():
                        borrow = BorrowBook.objects.get(reader = order.reader)
                        borrow.list_book.update(order.list_book)
                        borrow.save()
                        list_date = []
                        for i in order.list_book :
                            list_date.append(borrow.date_borrow)
                        list =  zip(borrow.list_book,borrow.list_book.values(),list_date)
                        borrow.save()
                    else :
                        borrow = BorrowBook()
                        borrow.reader = order.reader
                        borrow.list_book = order.list_book
                        borrow.save()
                    #Giam số lượng sách 
                    for i in order.list_book.keys():
                        book = Book.objects.get(bId = i)
                        book.number_of_book_remain -= 1
                        book.save()
                        
                    BorrowOrder.objects.filter(id=pk).delete()
                    messages.success(request,"Cập nhật phiếu đăng ký thành công.")

                    order.list_book.clear()
                return redirect('request_onl_list')
            except Exception as e:
                messages.error(request, e)
                return render(request, 'pages/librarian/update_status_request.html', context)
        return redirect('request_onl_list')
    context = {'form':form,'list':list}
    return render(request, 'pages/librarian/update_status_request.html', context)

def request_off(request):
    id = [1,2,3,4,5]
    context = {'id':id}
    if request.method == 'GET':
        try:
            form = request.GET
            myDict = dict(form.lists())
            context = {'id':id,'myDict':myDict}
            if myDict != {}:
                reader = Reader.objects.get(rId = myDict['rId'][0]) #mã reader
                if BorrowBook.objects.filter(reader=reader).exists() is True: 
                    borrow = BorrowBook.objects.get(reader = reader)  
                    for i in myDict.values():
                        if i[0] in borrow.list_book.keys(): 
                            messages.error(request,'Bạn đã mượn sách có mã {} trước đó'.format(i[0]))
                            return render(request,'pages/librarian/request_offline.html',context)
                        elif Book.objects.filter(bId = i[0]).exists() is True:
                                print('t')
                                borrow.list_book['{}'.format(i[0])] = '{}'.format(Book.objects.get(bId = i[0]))   
                                borrow.save()
                    return redirect('borrowers')
                else:                         
                    borrow = BorrowBook()
                    borrow.reader = reader
                    for i in myDict.values():
                        borrow.list_book['{}'.format(i[0])] = '{}'.format(Book.objects.get(bId = i[0]))
                    borrow.save()
                    return redirect('borrowers')
            return render(request,'pages/librarian/request_offline.html',context)
        except Exception as e:
            messages.error(request, e)
            return render(request,'pages/librarian/request_offline.html',context)
    return render(request,'pages/librarian/request_offline.html',context)
def borrow_detail(request,pk):
    borrow = BorrowBook.objects.get(id=pk)
    list =  zip(borrow.list_book,borrow.list_book.values())
    context = {'borrow':borrow,'list':list}
    return render(request,'pages/librarian/borrow_detail.html',context)

def get_all_borrowing_book_of_reader(list_book):
    res = None


    return res


def return_book(request,pk):

    borrow_detail = BorrowBook.objects.get(pk=pk)
    borrow_order = BorrowOrder.objects.filter(reader=borrow_detail.reader)
    
    today = datetime.datetime.now()
    
    list_book = [Book.objects.get(bId=bId) for bId, name in borrow_detail.list_book.items()]
    
    num_days_borrow = today - borrow_detail.date_borrow.replace(tzinfo=None)
    fine = 0
    if num_days_borrow.days > 4:
        fine = (num_days_borrow.days - 4)*1000

    # print(borrow_detail.list_book.pop('S000003'))

    if request.method == 'POST':
        
        action = request.POST


        # duyet sach trong list_book: Array[Book]
        for book in list_book:

            # Ma sach tam
            temp_bId = 'return{}'.format(book.bId)

            # Neu trong submit form co tra hoac bao mat
            if temp_bId in action:
                try:
                # neu tra sach
                    if action[temp_bId] == 'return':

                        print('return')

                        # lap phieu tra sach
                        return_book_model = ReturnBook(
                            reader=borrow_detail.reader,
                            book=book,
                            date_borrow=borrow_detail.date_borrow,
                            date_return=today,
                            fine=fine
                        )

                        # lap phieu phat
                        if fine > 0:
                            penalty_ticket_model = PenaltyTicket(
                                reader=borrow_detail.reader,
                                staff=request.user.customer.staff,
                                reason='Trả sách trễ',
                                fine=fine
                            )
                            penalty_ticket_model.save()
                        book.number_of_book_remain += 1
                        return_book_model.save()
                        book.save()

                    # mat sach
                    else:
                        if fine > 0:
                            penalty_ticket_model = PenaltyTicket(
                                    reader=borrow_detail.reader,
                                    staff=request.user.customer.staff,
                                    reason='Trả sách trễ + Làm mất sách',
                                    fine=fine + book.price
                                )
                        else:
                            penalty_ticket_model = PenaltyTicket(
                                    reader=borrow_detail.reader,
                                    staff=request.user.customer.staff,
                                    reason='Làm mất sách',
                                    fine=book.price
                                )
                        
                        
                        book.total -= 1
                        penalty_ticket_model.save()
                        book.save()
                    print(borrow_detail.list_book)  
                    borrow_detail.list_book.pop(book.bId)

                    if len(borrow_detail.list_book) == 0:
                        borrow_detail.delete()
                        return redirect('borrowers')
                    else:
                        borrow_detail.save()

                    for order in borrow_order:
                        try:
                            order.list_book.pop(book.bId)
                        except KeyError:
                            pass
                        if len(order.list_book) == 0:
                            order.delete()
                            return redirect('borrowers')
                        else:
                            order.save()

                except Exception as e:
                    messages.error(request, e)
                    
                return redirect('return_book', pk)
                

    context = {
        'borrow_detail':borrow_detail.list_book.items(),
        'date_borrow':borrow_detail.date_borrow,
        'today': today.strftime("%d/%m/%Y"),
        'num_days_borrow': num_days_borrow.days,
        'reader_id':borrow_detail.reader.rId,
        'fine':fine,
        'total_fine':fine*len(list_book)
        }
    return render(request,'pages/librarian/return_book.html', context)

def return_book_history(request):
    return_book_model = ReturnBook.objects.all()
    context = {
        'return_book_model':return_book_model
    }
    return render(request, 'pages/return_book_history.html', context)

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
        try:
            book_liquidation_form = BookLiquidationForm(request.POST)
            print(request.POST)
            action = request.POST.get('submit')
            if action == 'reconfirm':
                pass
            elif action == 'confirm':
                book_liquidation_form.save()
                messages.success(request,'Thanh lý thành công')
                return redirect('list_book')
        except Exception as e:
            messages.error(request, e)
            return render(request,'pages/stockkeeper/thanh_ly.html', context)

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
        try:
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save()
                book.nguoinhan = request.user.customer.staff
                book.number_of_book_remain = book.total
                book.save()
                messages.success(request, "Sách được thêm thành công với ID là " + book.bId)
                return redirect('list_book')
        except Exception as e:
            messages.error(request, e)
            redirect('add_book')

    context = {'form':form}
    return render(request, 'pages/stockkeeper/add_book.html', context)

#--THỦ QUỸ
def receipt_list(request):
    receipts = FineReceipt.objects.all()
    if 'rId' in request.POST:
        rId = request.POST.get('rId')
        reader = Reader.objects.filter(rId=rId).exists()
        if not reader:
                messages.error(request, 'Độc giả không tồn tại.')
                return redirect('receipt_list')
        else:
            reader = Reader.objects.get(rId=rId)
            request.session['rId'] = rId
            request.session['debt'] = reader.total_debt
            return redirect('add_receipt')

    context={'receipts':receipts}
    return render(request,'pages/cashier/receipt_list.html', context)

def add_receipt(request):
    form = ReceiptForm()
    if request.method == 'POST':
        try:
            form = ReceiptForm(request.POST)
            rId = request.session['rId']
            reader = Reader.objects.get(rId=rId)

            if form.is_valid():
                receipt = form.save()
                receipt.reader = reader
                receipt.staff = request.user.customer.staff
                receipt.debt_left = receipt.debt - receipt.proceeds
                receipt.save()

                # Cập nhật tiền nợ mới
                reader.total_debt = receipt.debt_left
                reader.save()

                messages.success(request, "Thu tiền phạt thành công.")
                return redirect('receipt_list')

        except Exception as e:
            messages.error(request, e)
            return redirect('add_receipt')
            
    context = {'form':form}
    return render(request,'pages/cashier/add_receipt.html', context)

def remove_receipt(request, receipt_pk):
    receipt = FineReceipt.objects.get(pk=receipt_pk)

    if request.method == 'POST':
        receipt.delete()
        messages.success(request, 'Xóa phiếu thu thành công.')
        return redirect('receipt_list')

    context = {
        'receipt':receipt
    }
    return render(request,'pages/cashier/remove_receipt.html',context)

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

        messages.success(request, 'Xóa nhân viên {} thành công '.format(name))
        return redirect('manager_dashboard')

    context={
        'staff':staff
    }

    return render(request, 'pages/manager/delete_staff.html', context)