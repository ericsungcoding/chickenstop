from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register_page', views.register_page),
    path('register', views.register),
    path('logout', views.logout),
    path('orders', views.orders),
    path('orders/account', views.account),
    path('orders/update', views.update),
    path('orders/order', views.order),
    path('orders/create_order', views.create_order),
    path('orders/checkout', views.checkout),
    path('orders/complete_order', views.complete_order),
    path('orders/<int:order_id>/like', views.like),
    path('orders/<int:order_id>/reorder', views.reorder),
]