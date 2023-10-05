from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData["email"])
        if not user:
            errors["login"] = "An account with this email does not exist"
        else:
            if not bcrypt.checkpw(postData["password"].encode(), user[0].password.encode()):
                errors["password"] = "Invalid email or password"
        return errors
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = 'First name is required'
        if len(postData['last_name']) < 1:
            errors['last_name'] = 'Last name is required'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['regex'] = 'Invalid email address'
        email_check = User.objects.filter(email=postData['email'])
        if email_check:
            errors['duplicate'] = 'An account with this email address already exists'
        if len(postData['address']) < 1:
            errors['address'] = 'Address is required'
        if len(postData['city']) < 1:
            errors['city'] = 'City is required'
        if len(postData['state']) < 2:
            errors['state'] = 'State must be at least 2 characters'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if not postData['password'] == postData['password_conf']:
            errors['match'] = 'Passwords do not match'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=20)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Order(models.Model):
    sandwich = models.CharField(max_length=50)
    pickles = models.CharField(max_length=3)
    side = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name='liked_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)