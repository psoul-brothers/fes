# coding: utf-8
from datetime import datetime

#from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from persol_users.models import PersolUser
from django.db.models import Q, Count

# アンケート
from questions.models import Question

@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=50)
    pass
    
    def __str__(self):  
        return self.name

class Event(models.Model):
    STATUS_CHOICES = (
        ("N","募集中"),
        ("E","終了")
    )
    author         = models.ForeignKey(PersolUser, verbose_name='作成者', related_name='author')
    event_name     = models.CharField('イベント名', max_length=200)
    event_image    = models.ImageField('イメージ画像', upload_to='event_image', blank=True)
    event_datetime = models.DateTimeField('日時',blank=True,null=True)
    event_location = models.CharField('開催場所', max_length=200, blank=True)
    num_of_members = models.IntegerField('募集人数')
    dead_line      = models.DateField('募集締切日')
    overview       = models.TextField('概要')
#    comment = models.ManyToManyField(Comment)
    like           = models.ManyToManyField(PersolUser,verbose_name='いいね', related_name='like')
    watch          = models.ManyToManyField(PersolUser,verbose_name='ウォッチ', related_name='Watch')
    members        = models.ManyToManyField(PersolUser)
    search_tag     = models.TextField('検索用タグ', blank=True, null=True)
    event_status   = models.CharField('イベントステータス', max_length=1, choices=STATUS_CHOICES, blank=True, null=True)
    
    # アンケート
    question_date  = models.OneToOneField(Question, related_name='event_date', blank=True, null=True)
    question_location  = models.OneToOneField(Question, related_name='event_location', blank=True, null=True)
    
    
    def __str__(self):  
        return self.event_name
    
    def nokori(self):
        now_member = self.members.count()
        return self.num_of_members - now_member

    def like_list(self):
        return self.like.all()
    
    def event_date(self):
        try:
            return self.event_datetime.strftime('%Y.%m.%d')
        except AttributeError:
            return ""

    def event_starttime(self):
        try:
            return self.event_datetime.strftime('%H:%M~')
        except AttributeError:
            return ""
        
    def nobreak_overview(self):
        return self.overview.replace("\n", "")
    
    def mailing_list(self):
        member_addr=[member.mail_address for member in self.members.all()]
        watcher_addr=[watcher.mail_address for watcher in self.watch.all()]
        ml=member_addr+watcher_addr
        return ml

"""
python manage.py makemigrations
python manage.py migrate
"""