from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse 
import os


# Create your views here.
from .models import PersolUser
from .forms import user_add_Form
from .forms import user_modify_Form

def index(request):
    user_list = PersolUser.objects.order_by('name')
    context = {'user_list': user_list}
    return render(request, 'persol_users/index.html', context)
    
def detail(request, user_id):
    user = get_object_or_404(PersolUser, pk=user_id)
    return render(request, 'persol_users/detail.html', {'user': user})
    
def user_add(request):
    f = user_add_Form()
    print "test!!!!!!!!!"
    return render(request, 'persol_users/user_add.html', {'form1': f})
    
def user_add_operation(request):
    if request.method == 'POST':
        form = user_add_Form(request.POST)
        if form.is_valid():
            try:
                data_tmp = request.FILES['data']
                
            except:
                data_tmp = ''
            
            finally:
                q = PersolUser(
                    employee_number = request.POST['employee_number']
                    , surname =  request.POST['surname']
                    , name =  request.POST['name']
                    , mail_address =  request.POST['mail_address']
                    , self_introduction_text =  request.POST['self_introduction_text']
                    , data =  data_tmp
                    )
                
                # for auth by tanaka
                q.set_password(request.POST['password'])
                
                
                q.save()
                return HttpResponseRedirect(reverse('persol_users:index'))
            
    else:
        form = user_add_Form()
        
    return render(request, 'persol_users/user_add.html', {'form1': form})

    
def user_modify(request):
   
    req_employee_number = request.user.employee_number
    user = get_object_or_404(PersolUser, employee_number=req_employee_number)
    
    if request.method == 'POST':
        try:
            tmp = user.data.path
            
        except:
            tmp = ""
            
        finally:
            f = user_modify_Form(request.POST, instance = user)
            if f.is_valid():
                f.save()
                
            try:
                data_tmp = request.FILES['data']
                
            except:
                data_tmp = ''
            
            finally:
                user.data = data_tmp
                user.save()
                
                if tmp:
                    os.remove(tmp)
                    
                return HttpResponseRedirect(reverse('persol_users:index'))

    else:
        f = user_modify_Form(instance=user)
        
    edit_context = {'form1': f, 'user': user}
    return render(request, 'persol_users/user_modify.html', context=edit_context)


