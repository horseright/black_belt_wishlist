from django.shortcuts import render, redirect, HttpResponse
from django.utils.dateparse import parse_date
from .models import User
import re
from django.contrib import messages
import bcrypt
from django.core.urlresolvers import reverse

NAME_REGEX = re.compile (r'^(.*?[a-zA-Z]){2,}.*$')
PASSWORD_REGEX = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')

def index(request):
    return render (request, 'login/index.html')

def logout(request):
    request.session.clear()
    return redirect(reverse('login:index'))

def login(request):
    if request.method =='POST':
        result = User.objects.login(username= request.POST['username'], password = request.POST['password'])
        if result[0]:
            request.session['user_id'] = result[1].id
            request.session['name'] = result[1].name
            request.session['username'] = result[1].username
            return redirect(reverse('wishlist:index'))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('login:index'))
    else:
        messages.add_message(request, messages.INFO, 'Please Try Again')
        return redirect(reverse('wishlist:index'))

def register(request):
    name = request.POST['name']
    username = request.POST['username']
    datehired = parse_date(request.POST['datehired'])
    password  = request.POST['password']
    confirm_password  = request.POST['confirm_password']
    errors=User.objects.register_valid(name,username,password,confirm_password)
    if len(errors)>0:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        password = password.encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.create (name = name, username = username, password = hashed, date_hired = datehired)
        user.save()
        request.session['user_id'] = user.id

        return redirect('/')
