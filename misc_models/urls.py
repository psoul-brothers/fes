from django.conf.urls import url

from . import comment_views

app_name = 'miscs'
urlpatterns = [
    url(r'^comments/$', comment_views.IndexView.as_view(), name='comment_index'),
    url(r'^comments/event/(?P<event_id>[0-9]+)/author/(?P<persoluser_id>[0-9]+)/new/$', comment_views.new, name='comment_new'),
    url(r'^comments/create/$', comment_views.create, name='comment_create'),
    # url(r'^(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),
    # url(r'^(?P<event_id>[0-9]+)/edit/$', views.event_edit, name='event_edit'),
    # url(r'^(?P<event_id>[0-9]+)/join/$', views.event_join, name='event_join'),
    # url(r'^(?P<event_id>[0-9]+)/join/$', views.event_like, name='event_like'),
    # url(r'^(?P<event_id>[0-9]+)/leave/$', views.event_leave, name='event_leave'),
    # url(r'^(?P<event_id>[0-9]+)/leave/$', views.event_delete, name='event_delete'),
    # url(r'^create_user/$', views.create_user, name='create_user'),
#    url(r'^(?Pevent_id>[0-9]+)/vote/$', views.vote, name='vote'),
]