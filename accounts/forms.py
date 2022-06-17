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
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].label = 'Tên'
        self.fields['reader_type'].label = 'Giới tính'
        self.fields['birth'].label = 'Ngày sinh'
        self.fields['address'].label = 'Địa chỉ'


class StaffForm(ModelForm):
    position = forms.ChoiceField(choices=[
            ('Manager', 'Trưởng phòng'),
            ('Staff', 'Nhân viên'), 
        ], 
        required=True)
    class Meta:
        model = Staff
        fields = '__all__'

        exclude = ['sId','user','force_password_change']
        widgets = {
            'birth': DateInput()
        }
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].label = 'Tên'
        self.fields['birth'].label = 'Ngày sinh'
        self.fields['address'].label = 'Địa chỉ'
        self.fields['profile_pic'].label = 'Ảnh đại diện'
        self.fields['profile_pic'].widget.clear_checkbox_label = 'Xóa'
        self.fields['profile_pic'].widget.initial_text  = 'Hiện tại'
        self.fields['profile_pic'].widget.input_text  = 'Chọn hình đại diện khác'
        self.fields['certificate'].label = 'Bằng cấp'
        self.fields['position'].label = 'Chức vụ'
        self.fields['service'].label = 'Bộ phận'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})




class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['bId','number_of_book_remain','nguoinhan','addDate']
        widgets = {
            'ctg': forms.CheckboxSelectMultiple()
        }
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if str(field) != 'ctg':
                self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

        # self.fields['ctg'].widget.attrs.update({'id':"ms",'multiple':"multiple"})
        # self.fields['ctg'].widget.attrs['multiple'] = True
        self.fields['ctg'].widget.attrs.update({'multiple': 'multiple'})

class OrderForm(ModelForm):
    class Meta:
        model = BorrowOrder
        fields = '__all__'
        exclude = ['list_book']
        
class BookLiquidationForm(ModelForm):
    class Meta:
        model = BookLiquidation
        fields = '__all__'

class ReceiptForm(ModelForm):
    class Meta:
        model = FineReceipt
        fields = ['debt', 'proceeds']