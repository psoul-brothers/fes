#coding:utf-8

from django import forms
from django.forms import ModelForm
from .models import PersolUser

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class user_add_Form(forms.Form):
    employee_number = forms.CharField(label='社員番号')
    password = forms.CharField(label='パスワード',widget=PasswordInput(attrs={
         'type':"text",
         'onfocus':"if (this.value == 'Password') this.value = '';",
         'onfocus':"type='Password'",
    }))
    surname = forms.CharField(label='姓')
    name = forms.CharField(label='名')
    mail_address = forms.EmailField(label='メールアドレス')
    self_introduction_text = forms.CharField(label='自己紹介メッセージ',widget=forms.Textarea)
    data = forms.FileField(label='画像',required=False)
    
class user_modify_Form(ModelForm):
    class Meta:
        model = PersolUser
        fields = [
            'employee_number', 'surname', 'name', 'mail_address', 
            'self_introduction_text', 'data'
        ]

    

