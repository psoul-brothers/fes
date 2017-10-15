# coding: utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from persol_users.models import PersolUser
from questions.models import Question
from .models import Event
from .forms import CreateForm, CreateUserForm, EventForm, SelectUserForm, LikeUserForm, EventsSearchForm
from django.template.loader import get_template

from datetime import datetime
import os


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
    # Sort order definition
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
        event_list = Event.objects.order_by('id').reverse()
# get each event
    latest_events    = event_list
    joing_events     = event_list.filter(Q(members = request.user.id))
    watching_events  = event_list.filter(Q(watch   = request.user.id))
    organized_events = event_list.filter(Q(author  = request.user.id))
    member_list      = PersolUser.objects.order_by('id')
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
            login_user = get_object_or_404(PersolUser, id=request.user.id)
            try : image = request.FILES['event_image']
            except : image = 'event_image/default.png'
            finally :
                new_event = Event(
                    author         = login_user,
                    event_name     = request.POST['event_name'], 
                    event_image    = image, 
                    event_location = request.POST['event_location'], 
                    num_of_members = request.POST['num_of_members'], 
                    dead_line      = request.POST['dead_line'],
                    overview       = request.POST['overview'],
                    search_tag     = request.POST['search_tag'],
                    # アンケート
                    question_date = None,
                    question_location = None,
                )
                if len(request.POST['event_datetime']) > 0:
                    new_event.event_datetime = request.POST['event_datetime']
    
                # アンケート作成
                if 'use_question_d' in request.POST:
                    qd = Question()
                    qd.update_from_posted_params('d', request.POST)
                    new_event.question_date = qd
                
                if 'use_question_l' in request.POST:
                    ql = Question()
                    ql.update_from_posted_params('l', request.POST)
                    new_event.question_location = ql

                new_event.save()
                new_event.members.add(new_event.author)
             
                return redirect('events:event_detail', event_id=new_event.id)
        else:
            return render(request, 'events/create.html', {'form': form,})
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
    if request.user != event.author : raise PermissionDenied
    if request.method == 'POST':
        try : old_image = event.event_image.path
        except : old_image = ''
        finally:
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()     # image以外をデータコミット
            try : image_tmp = request.FILES['event_image']
            except : image_tmp = 'event_image/default.png'
            finally:
                print
                event.event_image = image_tmp
                event.save()
                if old_image != '':
                    if old_image != os.getcwd() + '/media/event_image/default.png': #/home/ubuntu/workspace/media/event_image/default.png
                        os.remove(old_image)
                """
                send_mail(
                    subject
                    , message
                    , from_email
                    , recipient_list
                    , fail_silently=False
                    , auth_user=None
                    , auth_password=None
                    , connection=None
                )"""
#                send_to=['psoul.brothers@gmail.com','psoul.brothers+test1@gmail.com','psoul.brothers+test2@gmail.com']
                subject, send_to, send_from = u'イベント[{}]が更新されました。'.format(event.event_name), event.mailing_list(), 'from@example.com'
                mail_template=get_template('events/mail_tmp.txt')
                context = {
                    "event": event,
                }
                mail_body=mail_template.render({"event": event})
                send_mail(subject, mail_body, send_from, send_to, fail_silently=False)
                # アンケート変更
                if not 'use_question_d' in request.POST:
                    event.question_delete('d')
                else:
                    if not event.question_date:
                        qd = Question()
                        qd.save()
                        event.question_date = qd
                    event.question_date.update_from_posted_params('d', request.POST)

                if not 'use_question_l' in request.POST:
                    event.question_delete('l')
                else:
                    if not event.question_location:
                        ql = Question()
                        ql.save()
                        event.question_location = ql
                    event.question_location.update_from_posted_params('l', request.POST)
                    
                event.save()

                return redirect('events:event_detail', event_id=event_id) # POST 後のリダイレクト
    else:
        form = EventForm(instance=event) # 非束縛フォーム
        edit_context = {'form' : form, 'event' : event}
        return render(request, 'events/edit.html', context=edit_context)

@login_required
def event_join(request, event_id):
    target_event = get_object_or_404(Event, id=event_id)
    login_user = get_object_or_404(PersolUser, id=request.user.id)
    if request.POST['join'] == 'add':
        target_event.members.add(login_user)
        # ウォッチ中の場合は、ウォッチをはずす
        watcher = target_event.watch.filter( id=request.user.id)
        if login_user in watcher:
            target_event.watch.remove(login_user)
    elif request.POST['join'] == 'leave':
        target_event.members.remove(login_user)
#あとで消すテスト用
    elif  request.POST['join'] == 'new_member':
        target_event.members.add(login_user)
        if login_user in target_event.watch:
            target_event.watch.remove(login_user)
    return HttpResponseRedirect(request.META['HTTP_REFERER']) # リクエスト先にリダイレクト

@login_required    
def event_like(request, event_id):
    target_event = get_object_or_404(Event, id=event_id)
    login_user   = get_object_or_404(PersolUser, id=request.user.id)
    if request.POST['like'] == 'leave' :
        target_event.like.remove(login_user)
    elif request.POST['like'] == 'like':
        target_event.like.add(login_user) # 後で消す。テスト用
    else:
        target_event.like.add(login_user)
    return HttpResponseRedirect(request.META['HTTP_REFERER']) # リクエスト先にリダイレクト

@login_required
def event_watch(request, event_id):
    target_event = get_object_or_404(Event, id=event_id)
    login_user   = get_object_or_404(PersolUser, id=request.user.id)
    if request.POST['watch'] == 'leave':
        target_event.watch.remove(login_user)
    else:
        target_event.watch.add(login_user)
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
