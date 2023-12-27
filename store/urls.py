from django.urls import path
from .views import IndexView,SignupView, LoginView, LogoutView, CartView, CheckoutView, OrderView
from store.middlewares.authmiddle import auth_middleware

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('signup/',SignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='login'),
    path('orders/login/', LoginView.as_view(), name='orders_login'),
    path('logout/', LogoutView, name='logout'),
    path('cart/',CartView.as_view(), name='cart'),
    path('check-out/',auth_middleware(CheckoutView.as_view()), name='check-out'),
    path('orders/',auth_middleware(OrderView.as_view()), name='orders'),
]
