from django.contrib import admin
from .models import *

#   Register your models here.


admin.site.register(Category)
admin.site.register(Food)
admin.site.register(OrderItem)
admin.site.register(Order)
#admin.site.register(Checkout)
admin.site.register(Coupon)
#admin.site.register(Restuarant)
admin.site.register(Reservation)
#admin.site.register(Table)