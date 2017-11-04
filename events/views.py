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
            event_list = event_list.filter(
                Q(event_datetime__gte = datetime.now()) | #今日以降 または
                Q(event_datetime__isnull = True)          #日付がNULL
            ).order_by('event_datetime')
#            event_list = event_list.order_by('event_datetime')
        """降順指定したい場合
        if request.POST['sort'] == "desc":
            event_list = event_list.reverse()
        """
    else:
        search_word = ""
        event_list = Event.objects.order_by('id').reverse()
# get each event
    
    latest_events    = event_list.exclude( #以下を除く
        Q(author = request.user.id)           | #自分が主催者
        Q(members = request.user.id)          | #or自分がメンバーにいる
        Q(event_datetime__lt = datetime.now())| #or 開催日が今日以前
        Q(dead_line__lt = datetime.now())      | #or 募集締め切り日が今日以前
        Q(event_status = 'E')                   #or ステータスが募集終了
    )
    joing_events     = event_list.filter(Q(members = request.user.id)).order_by('event_datetime').reverse().exclude(
        Q(event_datetime__lt = datetime.now()) #開催日が今日以前を除く
    ) #日付昇順
    watching_events  = event_list.filter(
        Q(watch   = request.user.id)).order_by('event_datetime').reverse().exclude(Q(event_datetime__lt = datetime.now()) #開催日が今日以前を除く
    )
    organized_events = event_list.filter(Q(author  = request.user.id))
    old_events       = event_list.filter(Q(event_datetime__lt = datetime.now())).order_by('event_datetime')
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
        'organized_events' : organized_events,
        'old_events'       : old_events,
        'search_word'      : search_word
    }
#    return render(request, 'events/index.html', context)
    return render(request, 'events/new_index.html', context)

@login_required 
def event_create(request):
    """
    add new event.
    the event author is auto added to event.members.
    """
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
        form = EventForm() # 非束縛フォーム
        return render(request, 'events/create.html', {'form': form,})

@login_required
def event_detail(request, event_id):
    """
    Generate event detail page.
    """
    event   = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event,
    }
    return render(request, 'events/new_detail.html', context)

@login_required
def event_edit(request, event_id):
    """
    Generate event update page.
    Updating the event, then send to latest event infomations to members and watchers by e-mail.
    """
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
            except :
                image_tmp = event.event_image
            finally:
                event.event_image = image_tmp
                event.save()
                if old_image != '':
                    if old_image != event.event_image.path:
                        if old_image != os.getcwd() + '/media/event_image/default.png': #/home/ubuntu/workspace/media/event_image/default.png
                            os.remove(old_image)
                
#                send_to=['psoul.brothers@gmail.com','psoul.brothers+test1@gmail.com','psoul.brothers+test2@gmail.com']
                subject, list_of_mail_to, send_from = u'イベント[{}]が更新されました。'.format(event.event_name), event.mailing_list(), 'from@example.com'
                mail_template = get_template('events/mail_tmp.txt')
                context = {"event": event,}
                mail_body = mail_template.render({"event": event})
#               send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None)
                send_mail(subject, mail_body, send_from, list_of_mail_to, fail_silently=False)
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
    """
    add or remove login user to event.members.
    if that user is event watchers, remove from watchers.
    """
    target_event = get_object_or_404(Event, id=event_id)
    login_user = get_object_or_404(PersolUser, id=request.user.id)
    if request.POST['join'] == 'add':
        target_event.members.add(login_user)
        # ウォッチ中の場合は、ウォッチをはずす
        watcher = target_event.watch.filter(id=request.user.id)
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
    """
    add or remove login user to event.like!
    """
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
    """
    add or remove login user for event.wacth!
    """
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
    event = get_object_or_404(Event, pk=event_id)
    if request.user != event.author : raise PermissionDenied
    event.delete()
    return redirect('events:event_index') 
    
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
