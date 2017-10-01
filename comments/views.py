# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Comment
from .forms import CommentForm
from events.models import Event
from persol_users.models import PersolUser

from django.views import generic

class IndexView(generic.ListView):
    template_name = 'misc_models/index.html'
    context_object_name = 'all_comment_list'

    def get_queryset(self):
        return Comment.objects.all()

def new(request, event_id, persoluser_id):
    ev = get_object_or_404(Event, pk=event_id)
    athr = get_object_or_404(PersolUser, pk=persoluser_id)
    context={
        'form' : CommentForm(request.POST, instance=Comment(event=ev, author=athr)),
    }
    return render(request,'misc_models/comment_form.html',context)
    

def create(request):
    form = CommentForm(request.POST)
    form.save()
    return HttpResponseRedirect(reverse('miscs:comment_index'))
    
