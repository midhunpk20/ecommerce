from django.contrib import admin

# Register your models here.

from admin_app.models import *

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(ShippingAddress)