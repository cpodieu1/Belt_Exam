from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    
    def register_validator(self, post_data):
        errors = {}

        email_regex = re.compile(r'^[a-zA-Z0-9.+-_]+@[a-zA-Z0-9.-_]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data['email']):
            errors['email'] = 'Invalid email address.'

        if (len(post_data['first_name']) < 2):
            errors['first_name'] = 'First name should be 2 or more characters.'

        if (len(post_data['last_name']) < 2):
            errors['last_name'] = 'Last name should be 2 or more characters.'
        
        if (len(post_data['password']) < 8):
            errors['password'] = 'Password should be 8 or more characters.'
        
        if post_data['password'] != post_data['confirm_pw']:
            errors['password_match'] = 'Password and confirmed password do not match.'

        return errors

    def login_validator(self, post_data):
        errors = {}
        try:
            User.objects.get(email = post_data['email'])
            errors['email'] = 'This email is already a member.'
        except:
            pass 
        return errors
        # users = User.objects.filter(email=post_data['email])
        # if len(users) != 0:
            # erros['email] = 'This is email is already a member.'



class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=60)
    createed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class WishManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors['item'] = "Item must be no fewer than 3 characters."
        if len(postData['desc']) < 3:
            errors['first_name'] = "Description must be no fewer than 3 characters."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    email_hash = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="wishes", on_delete=models.CASCADE)

    objects = WishManager()


class Granted_wish(models.Model):
    item = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now=True)
    granted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes')
    user = models.ForeignKey(User, related_name="granted_wishes", on_delete=models.CASCADE)

    # @property
    def num_likes(self):
        return self.likes.all().count()
