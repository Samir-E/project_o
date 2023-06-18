from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Orders)
admin.site.register(OrderPosition)
admin.site.register(PositionInOrder)
# admin.site.register(Cart)
# admin.site.register(CartItem)
