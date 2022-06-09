from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class ReaderForm(ModelForm):
	class Meta:
		model = Reader
		fields = ['user','name','reader_type','address','email']		

class StaffForm(ModelForm):
	class Meta:
		model = Staff
		fields = '__all__'
		exclude = ['sId','user']

class CreateUserForm():
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = '__all__'
