from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
# from store.middlewares.authmiddle import auth_middleware
from django.http import Http404



def LogoutView(request):
  request.session.clear()
  return redirect('login')


class SignupView(View):
  def get(self, request):
    return render(request, 'signup.html')
  
  def post(self, request):
    data=request.POST
    username=data.get('username')
    phone=data.get('phone')
    email=data.get('email')
    password=data.get('password')

    #VALIDATIONS ------------------------------
    values={
      'username':username,
      'phone':phone,
      'email':email,
      'password':password
    }
    customer=Customer(username=username, phone=phone, email=email, password=password)

    if not username:
     messages.warning(request,"Username required!")
    elif not phone:
      messages.warning(request,"Phone required!")
    elif len(phone)!=10:
      messages.warning(request,"Phone should be of 10")
    elif not email:
      messages.warning(request,"Email required!")
    elif not password:
      messages.warning(request,"Password required!")
    elif len(password)<=10:
      messages.warning(request,"password must be of 10 or more")
    elif customer.customer_exists():
      messages.warning(request,"Account with this email already exist.")
    else:
      customer.password=make_password(customer.password)
      customer.save()
      messages.success(request,"Successfully registered")
      return redirect('login')
    data={'values':values}
    return render(request, 'signup.html', data)


class IndexView(View):
 def get(self, request):
  products=None
  products=Product.objects.all()
  categories=Category.objects.all()
  category_id=request.GET.get('category')
  if request.session.get('cart') is None:
    request.session['cart']=[]
  if category_id:
   products=Product.get_product_by_category_id(category_id)
  else:
   products=Product.objects.all()
  data={}
  data["products"]=products
  data["categories"]=categories

  print("you are", request.session.get('email'))
  return render(request, 'index.html', data)
 
 def post(self, request):
   product=request.POST.get('product')
   cart=request.session.get('cart')
   if cart:
     quantity=cart.get(product)
     if quantity:
       cart[product]=quantity+1
     else: 
       cart[product]=1
   else:
     cart={}
     cart[product]=1
   print(product)
   request.session['cart']=cart
   print("cart is ",request.session['cart'])
   return redirect('index')
 
class LoginView(View):
 return_url=None
 def get(self, request):
  LoginView.return_url=request.GET.get('return_url')
  return render(request, 'login.html')

 def post(self, request):
  username=request.POST.get('username')
  email = request.POST.get('email')
  password = request.POST.get('password')
  try:
    customer = Customer.objects.get(email=email)
  except Customer.DoesNotExist:
    messages.warning(request, 'Email/Password Incorrect..')
    return render(request, 'login.html', {'email': email})

  if check_password(password, customer.password):
     messages.success(request, 'Login successful!')

     request.session['customer_id'] = customer.id
     request.session['email']=email
     request.session['username']=username
     if LoginView.return_url:
       return HttpResponseRedirect(LoginView.return_url)
     else: 
      LoginView.return_url=None
      return redirect('index')  
  else:
    messages.warning(request, 'Email/Password Incorrect!')
    return render(request, 'login.html', {'email': email, 'username':username})


class CartView(View):
    def get(self, request):
        cart_items = request.session.get('cart', {})
        
        # Ensure that 'cart_items' is a dictionary
        if not isinstance(cart_items, dict):
            cart_items = {}  # If it's not a dictionary, set it to an empty dictionary
        
        ids = list(cart_items.keys())
        products = Product.get_products_by_id(ids)
        
        return render(request, 'cart.html', {'cart': cart_items, 'products': products})


class CheckoutView(View):
    def post(self, request):
        print("data is ", request.POST)
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, cart, products)

        for product in products:
            if customer_id is not None:
                order = Order(
                    customer=Customer(id=customer_id),
                    product=product,
                    price=product.price,
                    address=address,
                    phone=phone,
                    quantity=cart.get(str(product.id))
                )
                order.save()
            else:
                return redirect('login')

        request.session['cart'] = {}
        return redirect('orders')


class OrderView(View):
  def get(self, request):
    customer=request.session.get('customer_id')
    orders=Order.get_orders_by_customer(customer)
    print(orders)
    return render(request, 'orders.html', {'orders':orders})



