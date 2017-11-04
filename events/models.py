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
        ("E","募集終了")
    )
    author         = models.ForeignKey(PersolUser, verbose_name='作成者', related_name='author')
    event_name     = models.CharField('イベントタイトル', max_length=200)
    event_image    = models.ImageField('イメージ画像', upload_to='event_image', blank=True, null=True)
    event_datetime = models.DateTimeField('開催日時', null=True)
    event_location = models.CharField('開催場所', max_length=200, blank=True)
    num_of_members = models.IntegerField('募集人数')
    dead_line      = models.DateField('募集締切日', blank=True)
    overview       = models.TextField('イベント概要')
#    comment = models.ManyToManyField(Comment)
    like           = models.ManyToManyField(PersolUser,verbose_name='いいね', related_name='like')
    watch          = models.ManyToManyField(PersolUser,verbose_name='ウォッチ', related_name='Watch')
    members        = models.ManyToManyField(PersolUser)
    search_tag     = models.TextField('検索用タグ', blank=True, null=True)
    event_status   = models.CharField('イベントステータス', max_length=1, choices=STATUS_CHOICES, blank=False, null=False, default='N')
    
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
    
     
    # アンケート削除
    def question_delete(self, type):
        if type == 'd':
            q = self.question_date
            self.question_date = None
        elif type == 'l':
            q = self.question_location
            self.question_location = None
        
        if q:
            q.delete()
        
    # アンケート取得。なければデフォルト値のダミーアンケートを返す
    def question_date_or_dummy(self):
        qd = self.question_date
        if not qd:
            qd = Question.get_default_question('d')
        return qd
        
    def question_location_or_dummy(self):
        ql = self.question_location
        if not ql:
            ql = Question.get_default_question('l')
        return ql
        
    def mailing_list(self):
        member_addr=[member.mail_address for member in self.members.all()]
        watcher_addr=[watcher.mail_address for watcher in self.watch.all()]
        ml=member_addr+watcher_addr
        return ml
    
    def status(self):
        if self.event_status == "N": return "募集中"
        if self.event_status == "E": return "イベント終了"
        else:return ""

    def datetimeForIndex(self):
        if self.event_datetime:
            return self.event_datetime
        
        if not self.question_date:
            return "未定"
        else:
            return "アンケート中"

    def locationForIndex(self):
        if self.event_location:
            return self.event_location
        
        if not self.question_location:
            return "未定"
        else:
            return "アンケート中"

"""
python manage.py makemigrations
python manage.py migrate
"""