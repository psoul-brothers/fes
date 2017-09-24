#coding:utf-8

from django import forms
from django.forms import ModelForm
from .models import PersolUser

class user_add_Form(forms.Form):
    employee_number = forms.CharField(
            attrs={
             'value': "IDを入力してください",
             'onblur': "if (this.value == '') this.value = 'IDを入力してください';",
             'onfocus': "if (this.value == 'IDを入力してください') this.value = '';",
            }
        )
    surname = forms.CharField()
    name = forms.CharField()
    mail_address = forms.EmailField()
    self_introduction_text = forms.CharField(widget=forms.Textarea)
    image = forms.FileField(required=False)
    
class user_modify_Form(ModelForm):
    class Meta:
        model = PersolUser
        fields = [
            'employee_number', 'surname', 'name', 'mail_address', 
            'self_introduction_text', 'data'
        ]