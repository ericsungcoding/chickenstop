from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('/')
    user = User.objects.get(email=request.POST["email"])
    request.session["user_id"] = user.id
    return redirect('/orders')

def register_page(request):
    return render(request, 'register_page.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('/register_page')
    user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        address = request.POST['address'],
        city = request.POST['city'],
        state = request.POST['state'],
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
    )
    request.session['user_id'] = user.id
    return redirect('/orders')

def logout(request):
    request.session.flush()
    return redirect('/')

def orders(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'orders.html', context)

def account(request):
    context = {
        'user': User.objects.get(id=request.session["user_id"])
    }
    return render(request, 'account.html', context)

def update(request):
    user = User.objects.get(id=request.session["user_id"])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.address = request.POST['address']
    user.city = request.POST['city']
    user.state = request.POST['state']
    user.save()
    return redirect('/orders/account')

def order(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'order.html', context)

def create_order(request):
    request.session['sandwich'] = request.POST['sandwich']
    request.session['pickles'] = request.POST['pickles']
    request.session['side'] = request.POST['side']
    return redirect('/orders/checkout')

def checkout(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'checkout.html', context)

def complete_order(request):
    Order.objects.create(
        sandwich = request.POST['sandwich'],
        pickles = request.POST['pickles'],
        side = request.POST['side'],
        user = User.objects.get(id=request.session['user_id'])
    )
    return redirect('/orders')

def like(request, order_id):
    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=request.session['user_id'])
    user.liked_orders.add(order)
    return redirect('/orders')

def reorder(request, order_id):
    order = Order.objects.get(id=order_id)
    request.session['sandwich'] = order.sandwich
    request.session['pickles'] = order.pickles
    request.session['side'] = order.side
    return redirect('/orders/checkout')