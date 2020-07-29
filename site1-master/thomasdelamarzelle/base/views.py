from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .models import *
from .forms import ProductForm, CreateUserForm , StudentForm
from django.forms import inlineformset_factory
from .filters import ProductFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, authenticated_user


class Index(TemplateView):
    template_name = "index.html"


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

@unauthenticated_user
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
    logout(request)
    return redirect('index')


def register(request):
    form = CreateUserForm()
    form_extended = StudentForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form_extended = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            form_extended.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    context = {'form': form, 'form_extended': form_extended}

    return render(request, 'register.html', context)

@authenticated_user
def mydashboard(request):
    context = {}
    return render(request, 'mydashboard.html', context)

@authenticated_user
def account_settings(request):
    context = {}
    return render(request, 'account_settings.html', context)

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