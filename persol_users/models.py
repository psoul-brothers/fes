from __future__ import unicode_literals

from django.db import models

# Create your models here.


class PersolUser(models.Model):
    employee_number = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    Name = models.CharField(max_length=200)
    mail_address = models.EmailField(max_length=75)
    Self_introduction_text = models.CharField(max_length=200)
    