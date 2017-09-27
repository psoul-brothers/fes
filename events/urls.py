# coding: utf-8
from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    url(r'^$', views.event_index, name='event_index'),
    url(r'^create/$', views.event_create, name='event_create'),
    url(r'^(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),
    url(r'^(?P<event_id>[0-9]+)/edit/$', views.event_edit, name='event_edit'),
    url(r'^(?P<event_id>[0-9]+)/join/$', views.event_join, name='event_join'),
    url(r'^(?P<event_id>[0-9]+)/like/$', views.event_like, name='event_like'),
    url(r'^(?P<event_id>[0-9]+)/leave/$', views.event_leave, name='event_leave'),
    url(r'^(?P<event_id>[0-9]+)/leave/$', views.event_delete, name='event_delete'),
#    url(r'^create_user/$', views.create_user, name='create_user'), #もう使わない。イベントアプリ単体テスト用
    url(r'^search/$', views.event_search, name='event_search'),
#    url(r'^(?Pevent_id>[0-9]+)/vote/$', views.vote, name='vote'),
]