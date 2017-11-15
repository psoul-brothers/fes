from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse 
from django.contrib.auth.decorators import login_required
import os


# Create your views here.
from .models import PersolUser
from .forms import user_add_Form
from .forms import user_modify_Form
from django.conf import settings
DEFAULT_USER_IMG = 'user_image/default.png'


@login_required
def index(request):
    user_list = PersolUser.objects.order_by('name')
    context = {'user_list': user_list}
    return render(request, 'persol_users/index.html', context)

@login_required
def detail(request, user_id):
    reference_user = get_object_or_404(PersolUser, pk=user_id)
    
    req_employee_number = request.user.employee_number
    login_user = get_object_or_404(PersolUser, employee_number=req_employee_number)
    
    edit_context = {
        'reference_user'  : reference_user,
        'login_user' : login_user
    }
    return render(request, 'persol_users/detail.html', context=edit_context)


def user_add(request):
    f = user_add_Form()
    return render(request, 'persol_users/user_add.html', {'form1': f})


def user_add_operation(request):
    if request.method == 'POST':
        form = user_add_Form(request.POST)
        if form.is_valid():
            try:
                data_tmp = request.FILES['data']
                
            except:
                data_tmp = DEFAULT_USER_IMG
            
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
                return HttpResponseRedirect(reverse('portal'))
            
    else:
        form = user_add_Form()
        
    return render(request, 'persol_users/user_add.html', {'form1': form})


@login_required
def user_modify(request):
   
    user = request.user
    
    if request.method == 'POST':
        try:
            tmp = user.data.path
            
        except:
            tmp = ""
            
        finally:
            f = user_modify_Form(request.POST, instance = user)
            if f.is_valid():
                f.save()
            
    
            #password_tmp = request.POST['password']
            if request.POST['password'] :
                user.set_password(request.POST['password'])
                user.save()
    
            try:
                data_tmp = request.FILES['data']
                
            except:
                data_tmp = user.data
            
            finally:
                data_tmp2 = user.data
                user.data = data_tmp
                user.save()
                
                if tmp:
                    if tmp != os.path.join(settings.MEDIA_ROOT, DEFAULT_USER_IMG):
                        if data_tmp != data_tmp2:
                            os.remove(tmp)
                    
            return HttpResponseRedirect(reverse('portal'))

    else:
        f = user_modify_Form(instance=user)
        
    edit_context = {'form1': f, 'user': user}
    return render(request, 'persol_users/user_modify.html', context=edit_context)
    
    
@login_required
def reset_password(request, user_id):
    reference_user = get_object_or_404(PersolUser, pk=user_id)
    reference_user.set_password('password')
    reference_user.save()
    return HttpResponse("%s's password has been initialized." % reference_user.fullname())
