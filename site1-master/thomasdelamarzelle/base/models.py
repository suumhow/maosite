from django.db import models
from django.contrib.auth.models import User
# Choices
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
CATEGORY = (
    ('Ableton rack', 'Ableton rack'),
    ('Sample Pack', 'Sample Pack'),
    ('Lesson', 'Lesson'),
    ('Midi Pack', 'Midi Pack'),
)
STATUS = (
    ('Pending', 'Pending'),
    ('Out of Stock', 'Out of Stock'),
    ('Delivered', 'Delivered'),
)
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=60,default='placeholder', null=False)
    phone = models.CharField(max_length=60, null=True)
    profile_pic = models.ImageField(default='base/media/logo.jpg', null=True, blank=True,)
    gender = models.CharField(max_length=10, null=True, choices=GENDER)
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=240, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=240, null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2 )
    category = models.CharField(max_length=240, null=True, choices=CATEGORY)
    description = models.CharField(max_length=240, null=True)
    tags = models.ManyToManyField(Tags)
    profile_pic = models.ImageField(default='base/media/logo.jpg', null=True, blank=True, )
    digital = models.BooleanField(default=True, null=True, blank=False)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url





class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    email = models.EmailField()



    def __str__(self):
        representation = str(self.first_name) + str(self.last_name)
        return representation

class Order(models.Model):

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    transaction_id = models.CharField(max_length=100,blank=True, )
    complete = models.BooleanField(default=False, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True, null=True)


    def __str__(self):
        return str(self.transaction_id) + str(self.customer) + str(self.date_ordered)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital== False:
                shipping=True
        return shipping



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True )
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.product) +' ' + str(self.order) + ' ' + str(self.quantity) +' ' + str(self.date_added)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    ziploc = models.CharField(max_length=200, null=False)
    date_added = models.DateField(auto_now_add=True, null=True)
    country = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return str(self.customer) + str(self.address)






