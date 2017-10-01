# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from events.models import Event
from persol_users.models import PersolUser

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment_text = models.TextField()
