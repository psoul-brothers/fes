from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^(?P<comment_id>[0-9]+)/update$', views.update, name='update'),
]