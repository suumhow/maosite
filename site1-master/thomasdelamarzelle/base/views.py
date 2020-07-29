from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .models import *
from .forms import ProductForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import ProductFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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

def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('mydashboard')
        else:
            messages.info(request, 'Username Or password is incorrect')
    context = {}

    return render(request, 'login.html', context)

def logoutpage(request):
    return render(request, 'index.html')


def register(request):
    form = CreateUserForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    context = {'form': form}

    return render(request, 'register.html', context)

def mydashboard(request):
    context = {}
    return render(request, 'mydashboard.html', context)

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