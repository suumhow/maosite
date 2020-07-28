from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .models import *
from .forms import ProductForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import ProductFilter
from django.contrib.auth.forms import UserCreationForm


class Index(TemplateView):
    template_name = "index.html"

class Base(TemplateView):
    template_name = "base.html"

class Store(TemplateView):

    template_name = "store.html"

def product(request):
    form = ProductForm()
    context = {'form': form}
    if request.method == 'POST' :
        print('Printing post:', request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    return render(request, 'store.html', context)

def login(request):

    form = UserCreationForm()
    context = {'form': form}

    return render(request, 'login.html', context)


def register(request):
    form = CreateUserForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}

    return render(request, 'register.html', context)

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