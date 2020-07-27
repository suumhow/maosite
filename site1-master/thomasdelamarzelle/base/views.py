from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .models import *


class Index(TemplateView):
    template_name = "index.html"

class Base(TemplateView):
    template_name = "base.html"

class Store(TemplateView):

    template_name = "store.html"

def store(request):
    products = Product.objects.all()
    total_products = products.count()
    total_products_sample_pack = products.filter(category='Sample Pack').count()
    context = {'products': products, 'total_products':total_products,'total_products_sample_pack': total_products_sample_pack}
    return render(request, 'store.html', context)

def student(request, pk_test):
    student = Student.objects.get(id=pk_test)
    orders = student.order_set.all()
    total_orders = orders.count()
    context = {'student': student, 'orders': orders, 'total_orders': total_orders}
    return render(request, 'student.html', context)