from django.db import models
from .category import Category

class Product(models.Model):
 name=models.CharField(max_length=50)
 price =models.IntegerField()
 category=models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
 image=models.ImageField(upload_to="uploads/products")

 def __str__(self):
   return self.name

 @staticmethod
 def get_product_by_category_id(category_id):
   return Product.objects.filter(category=category_id)
 
 @staticmethod
 def get_products_by_id(ids):
   return Product.objects.filter(id__in=ids)
 
  