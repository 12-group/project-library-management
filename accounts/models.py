from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from .initial_func import pk_gen, staff_pk_gen, book_pk_gen
from django.contrib.postgres.fields import ArrayField

DEFAULT_PASSWORD = 'password'

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    birth = models.DateField(null=True, blank=True)
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
        return super().save(force_insert, force_update, using, update_fields)

class BookCategory(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):

    bId = models.CharField(default=book_pk_gen, primary_key=True, unique=True, max_length=255,editable=False)	
    name = models.CharField(max_length=200, null=True)
    cover_pic = models.ImageField(default="logo.png", null=True, blank=True)
    ctg = models.ManyToManyField(BookCategory, blank=True)							# Category
    author = models.CharField(max_length=200, null=True, blank=True)					# Author
    price = models.PositiveIntegerField(null=True, default=0)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    pubYear = models.PositiveIntegerField(default=datetime.date.today().year, validators=[MaxValueValidator(datetime.date.today().year+1), MinValueValidator(1500)])
    addDate = models.DateTimeField(null=True, auto_now_add=True)
    total = models.PositiveIntegerField(null=True, default=1)
    number_of_book_remain = models.PositiveIntegerField(null=True, default=1)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        if self.total < self.number_of_book_remain:
            raise ValueError('Số lượng sách còn lại không được lớn hơn tổng số lượng sách')

        return super().save(force_insert, force_update, using, update_fields)

    def get_all_ctg_to_string(self):
        all_this_book_ctg = self.ctg.all()
        return ', '.join([ctg.name for ctg in all_this_book_ctg])

class Cart(models.Model):
    reader = models.OneToOneField(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, blank=True)
class BorrowBook(models.Model):
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, blank=True)
    date_borrow = models.DateTimeField(null=True, auto_now_add=True)
    
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        if self.book != None:
            if self.book.number_of_book_remain == 0:
                raise ValueError('Sách ' + self.book.name + ' không còn')
            else:
                self.book.number_of_book_remain -= 1
                self.book.save()
        return super().save(force_insert, force_update, using, update_fields)
    
    def __str__(self):
        return self.reader.name + " " + self.book.name

class ReturnBook(models.Model):
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, blank=True)
    date_return = models.DateTimeField(null=True, auto_now_add=True)
    fine = models.PositiveIntegerField(null=True, default=0)

class FineReceipts(models.Model):
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)
    proceeds = models.PositiveIntegerField(null=True, default=0)
    date_pay_fine = models.DateTimeField(null=True, auto_now_add=True)
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        return super().save(force_insert, force_update, using, update_fields)


class PenaltyTicket(models.Model):
    reader = models.ForeignKey(Reader, null=True, on_delete=models.SET_NULL, blank=True)
    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)
    reason = models.CharField(max_length=200, null=True, blank=True)
    fine = models.PositiveIntegerField(null=True, default=0)
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None) -> None:
        return super().save(force_insert, force_update, using, update_fields)

class BookLiquidation(models.Model):
    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.PositiveIntegerField(null=True, default=0)
    reason = models.CharField(max_length=200, null=True, blank=True)
    date_liquidation = models.DateTimeField(null=True, auto_now_add=True)

class GetBook(models.Model):
    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.PositiveIntegerField(null=True, default=0)
    get_date = models.DateTimeField(null=True, auto_now_add=True)



