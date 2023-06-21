from django.contrib import admin

from .models import Orders, OrderPosition

# Register your models here.
admin.site.register(Orders)
admin.site.register(OrderPosition)
