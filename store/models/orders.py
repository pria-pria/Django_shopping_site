from django.db import models
from .product import Product
from .customer import Customer
from django.utils import timezone

class Order(models.Model):
 product=models.ForeignKey(Product, on_delete=models.CASCADE)
 customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
 quantity=models.IntegerField(default=1)
 price=models.IntegerField()
 address=models.CharField(max_length=100)
 phone=models.CharField(max_length=50)
 date=models.DateTimeField(default=timezone.now)
 status=models.BooleanField(default=False)

 def placeorder(self):
  self.save()


 @staticmethod
 def get_orders_by_customer(customer_id):
  return Order.objects.filter(customer=customer_id)