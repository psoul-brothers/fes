# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Event, Person
from persol_users.models import PersolUser
from django.db.models import Q
from .forms import CreateForm,CreateUserForm, EventForm, SelectUserForm, LikeUserForm, EventsSearchForm

from django.contrib.auth.decorators import login_required

@login_required
def event_index(request):
    latest_event_list = Event.objects.order_by('id')
    member_list = PersolUser.objects.order_by('id')
    form = SelectUserForm()
    like_form = LikeUserForm()
    context = {
        'latest_event_list': latest_event_list,
        'member_list': member_list,
        'form': form,
        'like_form':like_form
    }
    return render(request, 'events/index.html', context)
    
def event_create(request):
    #Event = get_object_or_404(Event, Event.id)
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid(): # バリデーションを通った
            # form.cleaned_data を処理
            # ...
            login_user = get_object_or_404(PersolUser, id=request.user.id)
            e = Event(
                author=login_user,
                event_name=request.POST['event_name'], 
                event_image=request.POST['event_image'], 
                event_datetime=request.POST['event_datetime'], 
                event_location=request.POST['event_location'], 
                num_of_members=request.POST['num_of_members'], 
                dead_line=request.POST['dead_line'],
                overview=request.POST['overview']
            )
            e.save()
#per                e.author.add(login_user)
            return HttpResponseRedirect('/events/') # POST 後のリダイレクト
    else:
        form = CreateForm() # 非束縛フォーム

    return render(request, 'events/create.html', {'form': form,})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    members_list = event.members.all()
    like_list = event.like.all()
    print(event.author.name)
    context = {
        'event': event,
        'memberslist':members_list,
        'like_list':like_list
    }
    return render(request, 'events/detail.html', context)


def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid(): # バリデーションを通った
            form.save()
            return HttpResponseRedirect('/events/' + event_id) # POST 後のリダイレクト
    else:
        form = EventForm(instance=event) # 非束縛フォーム

    edit_context = {'form': form, 'event': event}
    return render(request, 'events/edit.html', context=edit_context)


def event_join(request, event_id):
    target_event = get_object_or_404(Event, id=event_id)
    new_member = get_object_or_404(PersolUser, id=request.POST['new_members'])
    target_event.members.add(new_member)
    return HttpResponseRedirect('/events/')
    

def event_like(request, event_id):
    target_event = get_object_or_404(Event, id=event_id)
    new_like = get_object_or_404(PersolUser, id=request.POST['new_like'])
    target_event.like.add(new_like)
    return HttpResponseRedirect('/events/')

def event_leave(request, event_id):
    pass


def event_delete(request, event_id):
    pass

"""
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid(): # バリデーションを通った
            # form.cleaned_data を処理
            # ...
            e = Person(name=request.POST['name'])
            e.save()
            return HttpResponseRedirect('/events/') # POST 後のリダイレクト
    else:
        form = CreateUserForm() # 非束縛フォーム
    return render(request, 'events/create_user.html', {'form': form,})
"""

def event_search(request):
    if request.method == 'POST':
        form = EventsSearchForm(request.POST)
        if form.is_valid():
            tpl      = loader.get_template('events/index.html')
            word     = form.cleaned_data['word']
            print word
            search_results = Event.objects.filter(
                Q(event_name__contains = word) | 
                Q(overview__contains = word)
            )
            context = {
                'form'     : SelectUserForm(),
                'like_form':LikeUserForm(),
                'latest_event_list' : search_results
            }
            return render(request, 'events/index.html', context)
    else:
        form = EventsSearchForm()
    tpl = loader.get_template('events/index.html')
    return HttpResponse(tpl.render(RequestContext(
        request,
        {
            'form' : form
        }
    )))