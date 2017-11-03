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
    self_introduction_text = forms.CharField(label='自己紹介メッセージ',widget=forms.Textarea,required=False)
    data = forms.FileField(label='画像',required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        employee_number = cleaned_data.get('employee_number')
        mail_address = cleaned_data.get('mail_address')
        
        if employee_number is not None:
            if PersolUser.objects.filter(employee_number__contains = employee_number).exists():
                self._errors['employee_number'] = self.error_class(['ユーザーIDがすでに存在します'])  

        if mail_address is not None:
            if PersolUser.objects.filter(mail_address__contains = mail_address).exists():
                self._errors['mail_address'] = self.error_class(['メールアドレスがすでに存在します']) 
            
        return cleaned_data



class user_modify_Form(ModelForm):
    class Meta:
        model = PersolUser
        fields = ['surname', 'name', 'mail_address', 'self_introduction_text']

    password = forms.CharField(label='パスワード',widget=PasswordInput(attrs={
        'placeholder':'表示されません',
         'type':"text",
         'onfocus':"if (this.value == 'Password') this.value = '';",
         'onfocus':"type='Password'",
    }))
    data = forms.FileField(label='画像',required=False)    

    