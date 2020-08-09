from django.contrib import admin
from .models import *




# Register your models here.

admin.site.register(Student)
admin.site.register(Product)
#admin.site.register(Order)
admin.site.register(Tags)
admin.site.register(Customer)
#admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'complete', 'date_ordered', 'get_cart_items', 'shipping')
    ordering = ('date_ordered',)
    search_fields = ('customer', 'complete', 'date_ordered')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'date_added', 'get_total', 'quantity')
    ordering = ('order',)
    search_fields = ('order', 'product', )

