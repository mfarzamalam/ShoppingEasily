from django.contrib import admin
from .models import (Customer, Product, Cart, OrderPlaced)


# Register your models here.
@admin.register(Customer)
class Customer_Admin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']


@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discount_price','description','brand','category','product_image']


@admin.register(Cart)
class Cart_Admin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


@admin.register(OrderPlaced)
class OrderPlaced_Admin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status']