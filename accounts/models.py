from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

class Customer(models.Model):
	READER_TYPE = [
		('Nam', 'Nam'),
		('Nữ', 'Nữ')
	]

	user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	reader_type = models.CharField(max_length=200, null=True, choices=READER_TYPE, blank=True)
	birth = models.DateField(null=True, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	profile_pic = models.ImageField(default="profile_pic.png", null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class YearRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(YearRangeField, self).formfield(**defaults)

class BookCategory(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Book(models.Model):

	name = models.CharField(max_length=200, null=True)
	cover_pic = models.ImageField(default="logo.png", null=True,blank=True)
	ctg = models.ManyToManyField(BookCategory, blank=True)							# Category
	author = models.CharField(max_length=200, null=True, blank=True)					# Author
	price = models.PositiveIntegerField(null=True,blank=True)
	quantity = models.PositiveIntegerField(null=True,blank=True)
	publisher = models.CharField(max_length=200, null=True, blank=True)
	pubYear = models.PositiveIntegerField(default=datetime.date.today().year, validators=[MaxValueValidator(datetime.date.today().year+1), MinValueValidator(1500)])
	addDate = models.DateTimeField(null=True, auto_now_add=True)

	def __str__(self):
		return self.name