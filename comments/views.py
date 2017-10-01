# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Comment
from events.models import Event
from persol_users.models import PersolUser

from django.contrib.auth.decorators import login_required


@login_required
def index(request, event_id):
    ev = get_object_or_404(Event, pk=event_id)
    return render(request, 'comments/index.html', {'comments_list': ev.comment_set.all, 'event':ev})    

@login_required
def create(request, event_id):
    ev = get_object_or_404(Event, pk=event_id)
    txt = request.POST['comment_text_new']
    if len(txt.strip()) > 0:
        cmt = Comment(
            author=request.user,
            event=ev, 
            comment_text=txt
            )
        cmt.save()
        
    return redirect('comments:index', event_id=event_id )


@login_required
def update(request, event_id, comment_id):
    cmt = get_object_or_404(Comment, pk=comment_id)
    txt = request.POST['comment_text_update']
    if len(txt.strip()) > 0:
        cmt.comment_text = txt
        cmt.save()
    
    return redirect('comments:index', event_id=event_id )
    
