from django import template

register=template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
 if cart is None or not isinstance(cart, dict):
   return False
 keys=cart.keys()
 for id in keys:
  if int(id)== product.id:
   return True
 return False

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
 keys=cart.keys()
 for id in keys:
  if int(id)==product.id:
   return cart.get(id)
 return 0

@register.filter(name='price_total')
def price_total(product, cart):
 return product.price * cart_quantity(product, cart)


@register.filter(name='total_cart_price')
def total_cart_price(product, cart):
 sum=0
 for p in product:
  sum+=price_total(p, cart)
 return sum

@register.filter(name="currency")
def currency(number):
 return "₹ "+ str(number)

@register.filter(name="multiply")
def multiply(number, number1):
 return number * number1


