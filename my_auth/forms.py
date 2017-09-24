#coding:utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class MyAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={
             'value': "IDを入力してください",
             'onblur': "if (this.value == '') this.value = 'IDを入力してください';",
             'onfocus': "if (this.value == 'IDを入力してください') this.value = '';",
            }))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'span2','placeholder':'Password'}))