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
from django.http import JsonResponse
import json
import datetime


cartItems = 0


class Index(TemplateView):
    template_name = "index.html"

def index(request):
    user_auth = request.user.is_authenticated
    context = {'user_auth': user_auth, 'cartItems': cartItems}

    return render(request, 'index.html', context)


class Store(TemplateView):

    template_name = "store.html"

def product(request):
    user_auth = request.user.is_authenticated
    form = ProductForm()
    context = {'form': form, 'user_auth' : user_auth, 'cartItems': cartItems}
    if request.method == 'POST' :
        print('Printing post:', request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    return render(request, 'store.html', context)

@unauthenticated_user
def loginpage(request):
    user_auth = request.user.is_authenticated
    global cartItems
    cartItems=0

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('mydashboard')
        else:
            messages.info(request, 'Username Or password is incorrect')
    context = {'user_auth' : user_auth, 'cartItems': cartItems}

    return render(request, 'login.html', context)

def logoutpage(request):
    global cartItems
    cartItems = 0
    logout(request)
    return redirect('index', )

@unauthenticated_user
def register(request):
    user_auth = request.user.is_authenticated
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        #form_extended = StudentForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            '''first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            Student.objects.create(
                user=user,name=first_name + ' ' + last_name ,
            )'''
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form, 'user_auth' : user_auth, 'cartItems': cartItems}

    return render(request, 'register.html', context)

@authenticated_user
def mydashboard(request):
    user_auth = request.user.is_authenticated
    context = {'user_auth' : user_auth, 'cartItems': cartItems}
    return render(request, 'mydashboard.html', context)

@authenticated_user
def account_settings(request):
    user_auth = request.user.is_authenticated
    student_pro = request.user.student
    form = StudentForm(instance=student_pro)
    if request.method == 'POST':
        form = StudentForm(request.POST,request.FILES,  instance=student_pro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was updated')
            return redirect('account_settings')
    context = {'form': form, 'user_auth' : user_auth, 'cartItems': cartItems}

    return render(request, 'account_settings.html', context)

def store(request):
    global cartItems
    user_auth = request.user.is_authenticated
    if user_auth:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0, 'shipping':True}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    total_products = products.count()
    total_products_sample_pack = products.filter(category='Sample Pack').count()

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {'user_auth' : user_auth,
               'products': products,
               'total_products':total_products,
               'total_products_sample_pack': total_products_sample_pack,
               'myFilter': myFilter,
               'cartItems': cartItems}
    return render(request, 'store.html', context)



def student(request, pk_test):
    user_auth = request.user.is_authenticated
    student = Student.objects.get(id=pk_test)
    orders = student.order_set.all()
    total_orders = orders.count()
    context = {'student': student, 'orders': orders, 'total_orders': total_orders, 'user_auth' : user_auth, 'cartItems': cartItems}
    return render(request, 'student.html', context)

def cart(request):
    global cartItems
    user_auth = request.user.is_authenticated
    if user_auth:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']


    context = {'items' : items, 'user_auth' : user_auth, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    global cartItems
    user_auth = request.user.is_authenticated
    if user_auth:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']


    context = {'items' : items, 'user_auth' : user_auth, 'order': order, 'cartItems': cartItems, 'customer': customer}

    return render(request, 'checkout.html', context)

def updateItem(request):


    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:' , action)
    print('Action:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def processOrder(request):


    

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                ziplok=data['shipping']['ziploc'],
                country=data['shipping']['country'],
                )

    else:
        print('user not logged in')
    print('Data', request.body)
    return JsonResponse('Payment complete', safe=False)


