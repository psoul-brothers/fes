# coding: utf-8
from django import forms
from django.forms import ModelForm
from . import models
from persol_users import models as usermodels

from .models import Event
from persol_users.models import PersolUser

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'author', 'event_name', 'event_image', 'event_datetime', 
            'event_location', 'num_of_members', 'dead_line', 'overview'
        ]


class CreateForm(forms.Form):
    author = forms.CharField(max_length=200, label='作成者')
    event_name = forms.CharField(max_length=200, label='イベント名')
    event_image = forms.ImageField(required=False, label='イメージ画像')
    event_datetime = forms.DateTimeField(required=False, label='開催日時')
    event_location = forms.CharField(max_length=200, label='開催場所')
    num_of_members = forms.CharField(max_length=200, label='募集人数')
    dead_line = forms.DateField(label='募集締切日')
    overview = forms.CharField(max_length=2000, label='概要',widget=forms.Textarea)

class CreateUserForm(forms.Form):
    name = forms.CharField(max_length=100, label='ユーザ名')

from django.forms.models import ModelChoiceField
class CustomChoiceField(forms.ModelChoiceField):
    #ここで表示したい形式にします
    def label_from_instance(self, obj):
        return u'%s' % obj.name

class SelectUserForm(forms.Form):
    new_members = CustomChoiceField(
        queryset= usermodels.PersolUser.objects.all(),
        label='メンバー※後で消す',
        empty_label='選択してください',
        to_field_name='id',
        required=False
        )

class LikeUserForm(forms.Form):
    new_like = CustomChoiceField(
        queryset= usermodels.PersolUser.objects.all(),
        label='いいね※後で消す',
        empty_label='選択してください',
        to_field_name='id',
        required=False
        )

class EventsSearchForm(forms.Form):
    word = forms.CharField()
    