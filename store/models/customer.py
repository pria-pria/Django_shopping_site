from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Customer(models.Model):
 username=models.CharField(max_length=50)
 phone=models.CharField(max_length=10)
 email=models.EmailField()
 password=models.CharField(max_length=100)

 def __str__(self):
    return self.username

 def customer_exists(self):
   try:
    customer = Customer.objects.get(email=self.email)
    return True
   except ObjectDoesNotExist:
            return False


