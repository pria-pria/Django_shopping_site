from django.contrib import admin
from .models.category import Category
from .models.product import Product
from .models.customer import Customer
from .models.orders import Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
 list_display=['name', 'price', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
 list_display=['name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
 list_display=['username','email']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
 list_display=['product', 'customer']