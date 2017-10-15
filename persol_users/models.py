# coding: utf-8
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
    employee_number = models.CharField('社員番号',max_length=200, unique=True)
    surname = models.CharField('姓',max_length=200)
    name = models.CharField('名',max_length=200)
    mail_address = models.EmailField('メールアドレス',max_length=75, unique=True)
    self_introduction_text = models.CharField('自己紹介メッセージ',max_length=200)
    data = models.ImageField('画像',upload_to='user_image',blank=True)
    
    # for authentication by tnk
    USERNAME_FIELD = 'employee_number'
    objects = MyManager()

    def fullname(self):
        return self.surname + ' ' + self.name

