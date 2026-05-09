import django_filters
from n1.models import *
from rest_framework import filters


class customfilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(name__icontains='a')


class productfilter(django_filters.FilterSet):
    # name = django.filters.CharFilter(lookup_expr='icontains')
    # price = django.filters.NumberFilter()
    # price__gt = django.filters.NumberFilter(field_name='price', lookup_expr='gt')
    # price__lt = django.filters.NumberFilter(field_name='price', lookup_expr='lt')

    # class Meta:
    #     model = product
    #     fields = ['name', 'price', 'price__gt', 'price__lt']
    class Meta:
        model = na
        fields = {
            'name': ['exact', 'icontains'],
            # 'price': ['exact', 'gt', 'lt','range'],
        }
