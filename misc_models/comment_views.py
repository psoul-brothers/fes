# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response

from .models import Comment
from events.models import Event
from persol_users.models import PersolUser

def index(request):
    return HttpResponse('これはテスト用だよ')
