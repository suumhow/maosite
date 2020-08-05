import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
    cartItems = order['get_cart_items']
    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'digital': product.digital,
                    'description': product.description,
                    'imageURL': product.imageURL, },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request):
    user_auth = request.user.is_authenticated
    if user_auth:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        context = {'items': items, 'user_auth': user_auth, 'order': order, 'customer': customer, 'cartItems': cartItems}
    else:

        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        context = {'items' : items, 'user_auth' : user_auth, 'order': order, 'cartItems': cartItems, }
    return context


def guestOrder(request, data):
    print('user not logged in')
    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookiedData = cookieCart(request)
    items = cookiedData['items']
    customer, created = Customer.objects.get_or_create(
        email=email)
    customer.first_name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],

        )

    return customer, order