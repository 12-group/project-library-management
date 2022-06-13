import django_filters

from .models import *

class BookFilter(django_filters.FilterSet):
    class Meta:
        models = Book
        fields = {
            'name': ['icontains'], 
            'author': ['icontains'], 
            # 'ctg', 
            # 'pubYear'
        }