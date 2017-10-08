# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from .models import Event, Person
from persol_users.models import PersolUser
from django.db.models import Q, Count
from .forms import CreateForm,CreateUserForm, EventForm, SelectUserForm, LikeUserForm, EventsSearchForm
from datetime import datetime
import os

from django.contrib.auth.decorators import login_required

@login_required
def event_index(request):
    if request.method == 'POST':
        search_word = request.POST['word'] # 検索の値が空白でも大丈夫
        search_results = Event.objects.filter(
                Q(event_name__contains = search_word) | 
                Q(overview__contains   = search_word) |
                Q(search_tag__contains = search_word)
            )
        event_list = search_results
        if request.POST['sort'] == 'like':
            event_list = event_list.annotate(like_num = Count('like')).order_by('-like_num')
        elif request.POST['sort'] == 'watch':
            event_list = event_list.annotate(watch_num = Count('watch')).order_by('-watch_num')
        elif request.POST['sort'] == 'ascforday':
            event_list = event_list.filter(Q(event_datetime__gte = datetime.now())).order_by('event_datetime')
        """降順指定したい場合
        if request.POST['sort'] == "desc":
            event_list = event_list.reverse()
        """
    else:
        event_list = Event.objects.order_by('id')
    # get each event
    latest_events    = event_list
    joing_events     = event_list.filter(Q(members = request.user.id))
    watching_events  = event_list.filter(Q(watch   = request.user.id))
    organized_events = event_list.filter(Q(author  = request.user.id))
    
    member_list = PersolUser.objects.order_by('id')
    form = SelectUserForm()
    like_form = LikeUserForm()
    context = {
        'member_list'      : member_list,
        'form'             : form,
        'like_form'        : like_form,
        'latest_event_list': latest_events,
        'joing_events'     : joing_events,
        'watching_events'  : watching_events,
        'organized_events' : organized_events
    }
#    return render(request, 'events/index.html', context)
    return render(request, 'events/new_index.html', context)


@login_required 
def event_create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid(): # バリデーションを通った
            # form.cleaned_data を処理
            # ...
            login_user = get_object_or_404(PersolUser, id=request.user.id)
            try:
                image = request.FILES['event_image']
            except:
                image = 'event_image/default.png'
            finally:
                new_event = Event(
                    author         = login_user,
                    event_name     = request.POST['event_name'], 
                    event_image    = image, 
                    event_datetime = request.POST['event_datetime'], 
                    event_location = request.POST['event_location'], 
                    num_of_members = request.POST['num_of_members'], 
                    dead_line      = request.POST['dead_line'],
                    overview       = request.POST['overview'],
                    search_tag     = request.POST['search_tag']
                )
                new_event.save()
                return HttpResponseRedirect('/events/'+ str(new_event.id)) # 作成したイベントの詳細画面に
    else:
        form = CreateForm() # 非束縛フォーム
    return render(request, 'events/create.html', {'form': form,})

@login_required
def event_detail(request, event_id):
    event        = get_object_or_404(Event, pk=event_id)
    members_list = event.members.all()
    like_list    = event.like.all()
    num_of_like  = event.like.count()
    watcher_list = event.watch.all()
    context = {
        'event'       : event,
        'memberslist' : members_list,
        'like_list'   : like_list,
        'watcher_list': watcher_list,
        'num_of_like' : num_of_like
    }
#    return render(request, 'events/detail.html', context)
    return render(request, 'events/new_detail.html', context)
#    return render(request, 'events/Sample_detail.html', context)

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user != event.author: 
        raise PermissionDenied
    if request.method == 'POST':
        try: old_image = event.event_image.path
        except : old_image = ''
        finally:
            form = EventForm(request.POST, instance=event)
            if form.is_valid(): # バリデーションを通った
                form.save()     # image以外をデータコミット
            try:
                image_tmp = request.FILES['event_image']
            except:
                image_tmp = 'event_image/default.png'
            finally:
                event.event_image = image_tmp
                event.save()
                if old_image != '':
                    if old_image != os.getcwd() + '/media/event_image/default.png': #/home/ubuntu/workspace/media/event_image/default.png
                        os.remove(old_image)
                return HttpResponseRedirect('/events/' + event_id) # POST 後のリダイレクト
    else:
        form = EventForm(instance=event) # 非束縛フォーム
    edit_context = {
        'form'  : form,
        'event' : event
    }
    return render(request, 'events/edit.html', context=edit_context)

@login_required
def event_join(request, event_id):
    print "now1"
    target_event = get_object_or_404(Event, id=event_id)
    print "now2"
    if request.POST['join'] == 'add':
        print(request.user.id)
        new_member = get_object_or_404(PersolUser, id=request.user.id)
        target_event.members.add(new_member)
        # ウォッチ中の場合は、ウォッチをはずす
        watcher = target_event.watch.filter(id=request.user.id)
        if new_member in watcher:
            target_event.watch.remove(new_member)
    elif request.POST['join'] == 'leave':
        print "now3"
        out_member = get_object_or_404(PersolUser,id=request.user.id)
        target_event.members.remove(out_member)
#あとで消すテスト用
    elif  request.POST['join'] == 'new_member':
        new_member = get_object_or_404(PersolUser, id=request.POST['join'])
        target_event.members.add(new_member)
        if new_member in target_event.watch:
            target_event.watch.remove(new_member)
    return HttpResponseRedirect(request.META['HTTP_REFERER']) # リクエスト先にリダイレクト

@login_required    
def event_like(request, event_id):
    if request.POST['like'] == 'leave':
        target_event = get_object_or_404(Event, id=event_id)
        new_like = get_object_or_404(PersolUser, id=request.user.id)
        target_event.like.remove(new_like)
# 後で消す。テスト用
    elif request.POST['like'] == 'like':
        target_event = get_object_or_404(Event, id=event_id)
        new_like = get_object_or_404(PersolUser, id=request.POST['like'])
        target_event.like.add(new_like)
    else:
        target_event = get_object_or_404(Event, id=event_id)
        new_like = get_object_or_404(PersolUser, id=request.user.id)
        target_event.like.add(new_like)
    return HttpResponseRedirect(request.META['HTTP_REFERER']) # リクエスト先にリダイレクト

@login_required
def event_watch(request, event_id):
    if request.POST['watch'] == 'leave':
        target_event = get_object_or_404(Event, id=event_id)
        new_watch = get_object_or_404(PersolUser, id=request.user.id)
        target_event.watch.remove(new_watch)
    else:
        target_event = get_object_or_404(Event, id=event_id)
        new_watch = get_object_or_404(PersolUser, id=request.user.id)
        target_event.watch.add(new_watch)
        print(new_watch)
    return HttpResponseRedirect(request.META['HTTP_REFERER']) # リクエスト先にリダイレクト

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

@login_required
def event_search(request):
    if request.method == 'POST':
        form = EventsSearchForm(request.POST)
        if form.is_valid():
            word     = form.cleaned_data['word']
            search_results = Event.objects.filter(
                Q(event_name__contains = word) | 
                Q(overview__contains = word)
            )
            context = {
                'form'     : SelectUserForm(),
                'like_form': LikeUserForm(),
                'latest_event_list' : search_results
            }
            return render(request, 'events/index.html', context)
    else:
        form = EventsSearchForm()
    return render(request, 'events/index.html', {'form' : form})
