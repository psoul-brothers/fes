from __future__ import unicode_literals

from django.db import models
import uuid
import os

# for authentication by tnk
from django.contrib.auth.models import AbstractBaseUser
from my_auth.models import MyManager

# Create your models here.


class PersolUser(AbstractBaseUser):
    # for authentication by tnk(add 'unique'=True)
    employee_number = models.CharField(max_length=200, unique=True)
    surname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    mail_address = models.EmailField(max_length=75)
    self_introduction_text = models.CharField(max_length=200)
    data = models.ImageField(upload_to='user_image',blank=True)
    
    # for authentication by tnk
    USERNAME_FIELD = 'employee_number'
    objects = MyManager()



    def fullname(self):
        return self.surname + ' ' + self.name

