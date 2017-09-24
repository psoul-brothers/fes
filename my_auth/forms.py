#coding:utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class MyAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={
             'placeholder': "ID",
             'onblur': "if (this.value == '') this.value = 'ID';",
             'onfocus': "if (this.value == 'ID') this.value = '';",
            }))
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder':'Password',
         'type':"text",
         'onfocus':"if (this.value == 'Password') this.value = '';",
         'onfocus':"type='password'",
    }))