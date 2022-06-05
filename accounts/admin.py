from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Reader)
admin.site.register(Staff)
admin.site.register(BookCategory)
admin.site.register(Book)