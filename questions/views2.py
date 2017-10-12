#coding: utf-8
from django.shortcuts import get_list_or_404,get_object_or_404, render, redirect
from django.core.urlresolvers import reverse

from .models import Question,Choice,Answer
from events.models import Event

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


@login_required
def new(request, event_id, creation_type):
    # イベント作成者以外は403
    ev = get_event_or_403(request, event_id)

    question_date = Question() if 'd' in creation_type else None
    question_location = Question() if 'l' in creation_type else None
    return render(request, 'questions/new2.html', {'event': ev, 'question_date': question_date, 'question_location': question_location,})

@login_required
def create(request, event_id):
    # イベント作成者以外は403
    ev = get_event_or_403(request, event_id)
    
    if 'title_date' in request.POST:
        q = Question(questionnaire_title=request.POST['title_date'],
                    question_text=request.POST['text_date'])
        q.save()
        q.set_choices(request.POST['choices_date'])
        ev.question_date = q
        ev.save()

    if 'title_location' in request.POST:
        q = Question(questionnaire_title=request.POST['title_location'],
                    question_text=request.POST['text_location'])
        q.save()
        q.set_choices(request.POST['choices_location'])
        ev.question_location = q
        ev.save()


    return redirect('events:event_detail', event_id=event_id )

@login_required
def edit(request, event_id, edit_type):
    # イベント作成者以外は403
    ev = get_event_or_403(request, event_id)
    
    q = ev.question_date if edit_type == 'd' else ev.question_location
    if q is None:
        type = '日時' if edit_type == 'd' else '場所'
        q = Question(questionnaire_title = type + 'アンケート')
    return render(request, 'questions/edit2.html', {'event': ev, 'question': q, 'update_type':edit_type})


@login_required
def update(request, event_id, update_type):
    # イベント作成者以外は403
    ev = get_event_or_403(request, event_id)
    
    q = ev.question_date if update_type == 'd' else ev.question_location
    if q is None:
        q = Question()
    q.questionnaire_title = request.POST['title']
    q.question_text = request.POST['text']
    q.save()
    q.set_choices(request.POST['choices'])
    if update_type == 'd':
        ev.question_date = q
    else:
        ev.question_location = q
    
    ev.save()
    
    return redirect('events:event_detail', event_id=ev.id)
    

def get_event_or_403(request, event_id):
    # イベント作成者以外は403
    ev = get_object_or_404(Event, pk=event_id)
    if ev.author.id != request.user.id:
        raise PermissionDenied
    
    return ev
