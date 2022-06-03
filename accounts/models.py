from email.policy import default
from attr import field, fields
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Category_reader(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Customer(models.Model):
	user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	ctg = models.ManyToManyField(Category_reader)
	birth = models.DateTimeField(null=True)
	address = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
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

class Category_book(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Book(models.Model):
	name = models.CharField(max_length=200, null=True)
	cover_pic = models.ImageField(default="logo.png", null=True,blank=True)
	ctg = models.ManyToManyField(Category_book)							# Category
	auth = models.CharField(max_length=200, null=True)					# Author
	price = models.PositiveIntegerField(null=True,blank=True)
	amount = models.PositiveIntegerField(null=True,blank=True)
	publisher = models.CharField(max_length=200, null=True)
	pubYear = models.PositiveIntegerField(default=2022, validators=[MaxValueValidator(2022), MinValueValidator(1500)])
	inputDate = models.DateTimeField(null=True)

	def __str__(self):
		return self.name