from email import message
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from .initial_func import pk_gen, staff_pk_gen, book_pk_gen
from jsonfield import JSONField
# from django.utils.translation import gettext as _
from django.contrib import messages

DEFAULT_PASSWORD = 'password'

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    birth = models.DateField(null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default="profile_pic.png", null=True, blank=True)
    date_created = models.DateTimeField(null=True, auto_now_add=True)
        
    def __str__(self):
        return self.name


class Staff(Customer):
    CETIFICATE = [
        ('Baccalaureate', 'Tú tài'), 
        ('Intermediate', 'Trung cấp'), 
        ('College1', 'Cao đẳng'), 
        ('College2', 'Đại học'), 
        ('Master', 'Thạc sĩ'), 
        ('Doctor', 'Tiến sĩ')
    ]
    POSITION = [
        ('President', 'Giám đốc'), 
        ('Vice President', 'Phó giám đốc'), 
        ('Manager', 'Trưởng phòng'), 
        ('Deputy', 'Phó phòng'), 
        ('Staff', 'Nhân viên'), 
    ]
    SERVICE = [
        ('Librarian', 'Thủ thư'), 
        ('Cashier', 'Thủ quỹ'), 
        ('Stockkeeper', 'Thủ kho'), 
        ('Manager department', 'Ban giám đốc'), 
    ]
    certificate = models.CharField(max_length=200, null=True, choices=CETIFICATE, blank=True)
    position = models.CharField(max_length=200, null=True, choices=POSITION)
    service = models.CharField(max_length=200, null=True, choices=SERVICE)
    sId = models.CharField(default=staff_pk_gen, primary_key=True, unique=True, max_length=255,editable=False)
    force_password_change = models.BooleanField(default=True)

class Reader(Customer):
    READER_TYPE = [
        ('Male', 'Nam'), 
        ('Female', 'Nữ')
    ]

    reader_type = models.CharField(max_length=200, null=True, choices=READER_TYPE, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    rId = models.CharField(default=pk_gen, primary_key=True, unique=True, max_length=255,editable=False)	
    card_maker = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)
    total_debt = models.PositiveIntegerField(null=True, default=0)
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        # request = kwargs.get('request')
        # request = None
        # if self.request != None:
        #     request = self.request
        # else:
        #     request = kwargs.get('request')
        age = datetime.datetime.now().year - self.birth.year

        # # kiem tra xem tuoi cua doc gia co nam trong  18 den 55 khong
        # if age not in range(18, 56):
        #     messages.error(request, 'Tuổi của độc giả là {},độc giả phải có độ tuổi nằm trong 18 đến 55'.format(age))
        #     return None
                # kiem tra xem tuoi cua doc gia co nam trong  18 den 55 khong
        if age not in range(18, 56):
            raise Exception('Tuổi của độc giả là {},độc giả phải có độ tuổi nằm trong 18 đến 55'.format(age))


        return super().save(force_insert, force_update, using, update_fields)
    def is_out_of_date(self): # kiem tra xem the con han hay khong
        validate_value = datetime.datetime.now().month - self.date_created.month
        if validate_value > 6:
            return True
        return False



class BookCategory(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
# class MyMaxValueValidator(MaxValueValidator):
#     message = _('Năm xuất bản không hợp lệ %(limit_value)s.')
# class MyMinValueValidator(MinValueValidator):
#     message = _('Chỉ được nhận sách xuất bản trong vòng 8 năm (từ %(limit_value)s).')

class Book(models.Model):

    bId = models.CharField(default=book_pk_gen, primary_key=True, unique=True, max_length=255,editable=False)	
    name = models.CharField(max_length=200, null=True)
    cover_pic = models.ImageField(default="logo.png", null=True, blank=True)
    ctg = models.ManyToManyField(BookCategory, blank=True)							# Category
    author = models.CharField(max_length=200, null=True, blank=True)					# Author
    price = models.PositiveIntegerField(null=True, default=0)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    pubYear = models.PositiveIntegerField(
        null=True,
        validators=[MaxValueValidator(datetime.date.today().year+1), MinValueValidator(datetime.date.today().year-8)],
        )
    addDate = models.DateTimeField(null=True, auto_now_add=True)
    total = models.PositiveIntegerField(null=True, default=1)
    number_of_book_remain = models.PositiveIntegerField(null=True, default=1)
    description = models.CharField(max_length=200, null=True, blank=True)
    nguoinhan = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.name
    # def __init__(self, *args, **kwargs) -> None:
    #     self.request = None
    #     super().__init__(*args, **kwargs)
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        if self.total < self.number_of_book_remain:
            raise Exception('Số lượng sách còn lại không được lớn hơn tổng số lượng sách')
        return super().save(force_insert, force_update, using, update_fields)

    def get_all_ctg_to_string(self):
        all_this_book_ctg = self.ctg.all()
        return ', '.join([ctg.name for ctg in all_this_book_ctg])
class Cart(models.Model):
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, unique=False,  blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, blank=True)
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:

        carts = Cart.objects.filter(reader=self.reader)

        if carts.count() >= 5:
            raise Exception('Độc giả chỉ được mượn tối đa 5 quyển sách một lúc')
        
        borrow_orders = BorrowOrder.objects.filter(reader=self.reader)
        
        count_books = 0
        for borrow_order in borrow_orders:
            print(borrow_order.list_book)
            if borrow_order.status == 'Chờ xác nhận':
                count_books += len(borrow_order.list_book)
        borrow_book = BorrowBook.objects.filter(reader=self.reader)
        for book in borrow_book:
            count_books += len(book.list_book)
        if count_books >= 5:
            print('raise exception')
            raise Exception('Độc giả chỉ được mượn tối đa 5 quyển sách một lúc')


        return super().save(force_insert, force_update, using, update_fields)

class BorrowOrder(models.Model):
    STATUS = [
        ('Chờ xác nhận','Chờ xác nhận'),
        ('Đang soạn sách', 'Đang soạn sách'), 
        ('Hoàn thành', 'Hoàn thành'),
        ('Đã nhận sách','Đã nhận sách')
    ]
    #cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL, unique=False,  blank=True)
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, unique=False,  blank=True)
    list_book = JSONField()
    status = models.CharField(max_length=200, null=True, choices=STATUS, blank=True,default='Chờ xác nhận')

    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:

        borrow_orders = BorrowOrder.objects.filter(reader=self.reader)
        
        # count_books = 0
        # for borrow_order in borrow_orders:
        #     print(borrow_order.list_book)
        #     count_books += len(borrow_order.list_book)

        # if count_books >= 5:
        #     print('raise exception')
        #     raise Exception('Độc giả chỉ được mượn tối đa 5 quyển sách một lúc')

        return super().save(force_insert, force_update, using, update_fields)


class BorrowBook(models.Model):
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    list_book = JSONField()
    date_borrow = models.DateTimeField(null=True, auto_now_add=True)
    
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        
        if self.reader.is_out_of_date():
            raise Exception('Thẻ quá hạn')
        

        return super().save(force_insert, force_update, using, update_fields)
    
    def __str__(self):  
        return self.reader.name
    
class ReturnBook(models.Model):
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, blank=True)
    date_borrow = models.DateTimeField(null=True, auto_now_add=True)
    date_return = models.DateTimeField(null=True, auto_now_add=True)
    fine = models.PositiveIntegerField(null=True, default=0)
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        return super().save(force_insert, force_update, using, update_fields)

class FineReceipt(models.Model):
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    debt = models.PositiveIntegerField(null=True, default=0)
    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)
    proceeds = models.PositiveIntegerField(null=True, default=0)
    debt_left = models.PositiveIntegerField(null=True, default=0)
    date_pay_fine = models.DateTimeField(null=True, auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        # Kiểm tra tiền thu không vượt quá tiền mượn
        if self.proceeds > self.debt:
            raise Exception('Tiền thu không được vượt quá tiền nợ.')
            
        return super().save(force_insert, force_update, using, update_fields)

class PenaltyTicket(models.Model):
    # REASON = [
    #     ('return_late', 'Trả sách trễ'),
    #     ('lost', 'Mất sách'),
    # ]
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)
    reason = models.CharField(max_length=200, null=True, blank=True)
    fine = models.PositiveIntegerField(null=True, default=0)
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        self.reader.total_debt += self.fine
        self.reader.save()
        return super().save(force_insert, force_update, using, update_fields)

class BookLiquidation(models.Model):
    REASON = [
        ('lost','Mất'),
        ('damaged', 'Hư hỏng'), 
        ('user_lost', 'Người dùng làm mất'),
    ]
    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.PositiveIntegerField(null=True, default=1)
    reason = models.CharField(max_length=200, null=True, choices=REASON)
    date_liquidation = models.DateTimeField(null=True, auto_now_add=True)


    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        if self.quantity > self.book.number_of_book_remain:
            raise Exception('Không thể thanh lý nhiều hơn {} quyển sách'.format(self.book.number_of_book_remain))
        else:
            self.book.number_of_book_remain -= self.quantity
            self.book.total -= self.quantity
            self.book.save()
        return super().save(force_insert, force_update, using, update_fields)
