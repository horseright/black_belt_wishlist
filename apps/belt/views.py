from django.shortcuts import render, redirect
from ..login.models import User
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Product

def index(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
    'products':user.product_set.all().exclude(adder__id = request.session['user_id']),
    'myproducts':Product.objects.filter(adder__id=request.session['user_id']),
    'otherproducts':Product.objects.exclude(adder__id=request.session['user_id']),
    }
    return render (request, 'belt/index.html', context)

def create(request):
    return render(request, 'belt/create.html')

def add(request):
    if request.method != 'POST':
        return redirect(reverse('wishlist:index'))
    pname = request.POST['product']
    if len(pname) < 3:
        messages.error('Product name must be longer than 3')
        return redirect(reverse('wishlist:create'))
    user = User.objects.get(id=request.session['user_id'])
    try:
        p = Product.objects.get (name = pname)
    except:
        p = Product.objects.create(name = pname, adder = user)
    p.users.add(user)
    return redirect(reverse('wishlist:index'))

def product(request,id):
    try:
        p = Product.objects.get(id=id)
    except:
        return redirect(reverse('wishlist:index'))
    context = {
    'users':p.users.all(),
    'name':p.name
    }
    return render(request, 'belt/product.html', context)

def removeproduct(request,id):
    try:
        p = Product.objects.get(id=id)
    except:
        return redirect(reverse('wishlist:index'))
    user = User.objects.get(id=request.session['user_id'])
    p.users.remove(user)
    return redirect(reverse('wishlist:index'))

def addproduct(request,id):
    try:
        p = Product.objects.get(id=id)
    except:
        return redirect(reverse('wishlist:index'))
    user = User.objects.get(id=request.session['user_id'])
    p.users.add(user)
    # p.save()
    return redirect(reverse('wishlist:index'))
    
def delete(request,id):
    try:
        p = Product.objects.get(id = id)
    except:
        return redirect(reverse('wishlist:index'))
    if p.adder.id != request.session['user_id']:
        return redirect(reverse('wishlist:index'))
    p.delete()
    return redirect(reverse('wishlist:index'))
