# coding:utf-8
from __future__ import unicode_literals

from django.db import models

from events.models import Event
from persol_users.models import PersolUser

class Comment(models.Model):
    author = models.ForeignKey(PersolUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment_text = models.TextField()

class EventStatus(models.Model):
    status_name = models.CharField('ステータス名', max_length=64)
    
class Tag(models.Model):
    tag_name = models.CharField('タグ',max_length=128)
