# coding: utf-8
import datetime

#from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=50)
    pass
    
    def __str__(self):  
        return self.name

class Event(models.Model):
    author = models.CharField('作成者', max_length=200)
    event_name = models.CharField('イベント名', max_length=200)
    event_image = models.ImageField('イメージ画像',blank=True)
    event_datetime = models.DateTimeField('日時',blank=True,null=True)
    event_location = models.CharField('開催場所', max_length=200)
    num_of_members = models.CharField('募集人数', max_length=200)
    dead_line = models.DateField('募集締切日')
    overview = models.TextField('概要')
#    comment = models.ManyToManyField(Comment)
#    like = models.ManyToManyField(Person)
    members = models.ManyToManyField(Person)
#    tag = models.ManyToManyField(Tag)
#    event = models.OneToOneField(Status)
    
    def __str__(self):  
        return self.event_name
