from email.policy import default
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile_pic.png", null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Book(models.Model):
	name = models.CharField(max_length=200, null=True)
	ctg = models.CharField(max_length=200, null=True)					# Category
	auth = models.CharField(max_length=200, null=True)					# Author
	price = models.PositiveIntegerField(null=True,blank=True)
	amount = models.PositiveIntegerField(null=True,blank=True)
	publisher = models.CharField(max_length=200, null=True)
	pubYear = models.DateTimeField(null=True)

	def __str__(self):
		return self.name