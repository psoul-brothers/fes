from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^comments/$', views.IndexView.as_view(), name='comment_index'),
    url(r'^comments/event/(?P<event_id>[0-9]+)/author/(?P<persoluser_id>[0-9]+)/new/$', views.new, name='comment_new'),
    url(r'^comments/create/$', views.create, name='comment_create'),
]