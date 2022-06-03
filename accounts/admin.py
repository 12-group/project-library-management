from django.contrib import admin

import accounts

# Register your models here.

from .models import *

admin.site.register(Category_reader)
admin.site.register(Customer)
admin.site.register(Category_book)
admin.site.register(Book)