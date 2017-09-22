from django import forms

class user_add_Form(forms.Form):
    employee_number = forms.CharField()
    surname = forms.CharField()
    name = forms.CharField()
    mail_address = forms.EmailField()
    self_introduction_text = forms.CharField(widget=forms.Textarea)
    image = forms.FileField(required=False)
    
    