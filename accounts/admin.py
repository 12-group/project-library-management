from django.contrib import admin

import accounts

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Book)