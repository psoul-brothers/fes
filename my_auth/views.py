from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from forms import MyAuthForm

def login(request):
    form = MyAuthForm(request)
    return render(request, 'my_auth/login.html',{'form':form})
    
    
 
