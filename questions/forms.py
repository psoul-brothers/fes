#coding: utf-8
from django import forms
from django.contrib.admin import widgets
import os

ANSWER_CHOICES = {
    ('0','○'),
    ('1','△'),
    ('2','×'),
}

class AnswerForm(forms.Form):
    select_answer = forms.ChoiceField(label='属性', widget=forms.RadioSelect, choices= ANSWER_CHOICES, initial=0)