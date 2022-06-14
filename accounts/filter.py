import django_filters
from django import forms

from .models import *



class BookFilter(django_filters.FilterSet):
    min_year = django_filters.NumberFilter(
        field_name="pubYear", 
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={"class":"form-control"})
        )
    max_year = django_filters.NumberFilter(
        field_name="pubYear", 
        lookup_expr='lte',
        widget=forms.NumberInput(attrs={"class":"form-control"})
        )
    ctg = django_filters.ModelMultipleChoiceFilter(
        field_name="ctg",
        widget=forms.CheckboxSelectMultiple(attrs={"class":"form-check-label"}),
        queryset=BookCategory.objects.all()
    )
    class Meta:
        model = Book
        fields = {
            'name',
            'author',
            'ctg',
            }
        filter_overrides = {
        models.CharField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda f: {
                'lookup_expr': 'icontains',
                'widget': forms.TextInput(attrs={'class': 'form-control'})
            },
        },
        }

class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = Staff
        fields = {
            'sId',
            'name',
            'certificate',
            'position',
            'service'
        }