from django import forms

class user_add_Form(forms.Form):
    employee_number = forms.CharField()
    Surname = forms.CharField()
    Name = forms.CharField()
    mail_address = forms.EmailField()
    Self_introduction_text = forms.CharField()
    
    
    