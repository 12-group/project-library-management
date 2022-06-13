from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import *

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class DateInput(forms.DateInput):
    input_type = 'date'

class ReaderForm(ModelForm):
	class Meta:
		model = Reader
		fields = ['name','reader_type','address','birth','email']
		widgets = {
            'birth': DateInput()
        }
		

class StaffForm(ModelForm):
	class Meta:
		model = Staff
		fields = '__all__'

		exclude = ['sId','user','force_password_change']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = '__all__'
		exclude = ['bId','number_of_book_remain','nguoinhan','addDate']
		widgets = {
			'ctg': forms.CheckboxSelectMultiple()
		}

class BookLiquidationForm(ModelForm):
	class Meta:
		model = BookLiquidation
		fields = ['book', 'quantity', 'reason']
		widgets = {
			'reason': forms.TextInput(attrs={'class': 'textarea'})
		}