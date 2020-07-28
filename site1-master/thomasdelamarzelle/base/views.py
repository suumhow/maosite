from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .models import *
from .forms import StudentForm
from django.forms import inlineformset_factory
from .filters import ProductFilter


class Index(TemplateView):
    template_name = "index.html"

class Base(TemplateView):
    template_name = "base.html"

class Store(TemplateView):

    template_name = "store.html"

def register(request):
    form = StudentForm()
    context = {'form': form}
    if request.method == 'POST' :
        print('Printing post:', request.POST)
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    return render(request, 'register.html', context)

def login(request):
    #form = StudentForm()
    context = {'form': form}

    return render(request, 'login.html', context)


def store(request):
    products = Product.objects.all()
    total_products = products.count()
    total_products_sample_pack = products.filter(category='Sample Pack').count()

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {'products': products, 'total_products':total_products,'total_products_sample_pack': total_products_sample_pack, 'myFilter': myFilter}
    return render(request, 'store.html', context)

def student(request, pk_test):
    student = Student.objects.get(id=pk_test)
    orders = student.order_set.all()
    total_orders = orders.count()
    context = {'student': student, 'orders': orders, 'total_orders': total_orders}
    return render(request, 'student.html', context)