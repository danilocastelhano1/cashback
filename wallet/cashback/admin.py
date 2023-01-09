from django.contrib import admin

# Register your models here.
from .models import Cashback
from .models import Customer
from .models import Products

admin.site.register(Cashback)
admin.site.register(Customer)
admin.site.register(Products)
