from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


# Create your views here.
from .models import PersolUser
from .forms import user_add_Form

def index(request):
    user_list = PersolUser.objects.order_by('name')
    context = {'user_list': user_list}
    return render(request, 'persol_users/index.html', context)
    
def detail(request, user_id):
    user = get_object_or_404(PersolUser, pk=user_id)
    return render(request, 'persol_users/detail.html', {'user': user})
    
def user_add(request):
    f = user_add_Form()
    return render(request, 'persol_users/user_add.html', {'form1': f})
    
def user_add_operation(request):
    if request.method == 'POST':
        form = user_add_Form(request.POST)
        if form.is_valid():
            q = PersolUser(
                employee_number = request.POST['employee_number']
                , surname =  request.POST['surname']
                , name =  request.POST['name']
                , mail_address =  request.POST['mail_address']
                , self_introduction_text =  request.POST['self_introduction_text']
                , data = request.FILES['image']
                )
            
            # for auth by tanaka
            q.set_password('pass-123')
            
            
            q.save()
            return HttpResponseRedirect(reverse('persol_users:index'))
            
    else:
        form = user_add_Form()
        
    return render(request, 'persol_users/user_add.html', {'form1': form})

    
def user_modify(request, user_id):
    user = get_object_or_404(PersolUser, pk=user_id)
    
    f = user_modify_Form(instance=user)
    return render(request, 'persol_users/user_modify.html', {'from1': f})