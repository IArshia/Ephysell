from django.contrib import admin
from . models import Account, Game, Cart, CartItem, Order,OrderItem
admin.site.register(Account)
admin.site.register(Game)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

# Register your models here.
