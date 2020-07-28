import django_filters
from .models import *
from django_filters import DateFilter, CharFilter

class ProductFilter(django_filters.FilterSet):
    price_lower_then = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['name', 'price_lower_then', 'category', 'tags'] #'__all__' exclude = ['fgdsgds','sdf']