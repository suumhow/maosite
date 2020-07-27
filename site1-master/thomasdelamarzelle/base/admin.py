from django.contrib import admin
from .models import Student, Product, Order, Tags




# Register your models here.

admin.site.register(Student)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tags)