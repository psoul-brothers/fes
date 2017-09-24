# coding: utf-8
from django import forms
from django.forms import ModelForm
from . import models

from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['event','author','comment_text']
