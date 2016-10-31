from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile (r'^(.*?[a-zA-Z]){2,}.*$')
PASSWORD_REGEX = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')

class UserManager(models.Manager):
    def login(self, **kwargs):
      if kwargs is not None:
        errors = { }
        if len(kwargs['password']) ==0:
          errors['password'] = "Please Enter a Password"
        if len(kwargs['username']) ==0:
          errors['username'] = "Please Enter a username"
        if len(errors)!=0:
          return (False, errors)
        else:
          user = self.filter (username = kwargs['username'])
          if not user:
            errors['user'] = "username/password combination not found"
            return (False, errors)
          else:
            if bcrypt.checkpw(kwargs['password'].encode('utf-8'), user[0].password.encode('utf-8')):
              return (True, user[0])
            else:
              errors['user'] = 'username/Password Combination Not Found'
              return (False, errors)

    def register_valid(self,name,username,password,confirm_password):
          error=[]
          if not NAME_REGEX.match(name):
              error.append("name invalid")
          if not NAME_REGEX.match(username):
              error.append("username invalid")
          if not PASSWORD_REGEX.match(password):
              error.append("password too short")
          if confirm_password != password:
              error.append("password is not consistent")
          return error

class User (models.Model):
    name = models.CharField (max_length = 45)
    username = models.CharField (max_length = 45)
    password = models.CharField (max_length = 200)
    date_hired = models.DateField (null = True)
    created_at = models.DateField (auto_now_add = True)
    updated_at = models.DateField (auto_now = True)
    objects = UserManager()
