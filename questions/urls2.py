from django.conf.urls import url

from . import views2

app_name = 'event_questions'
urlpatterns = [
    url(r'^new/(?P<creation_type>d?l?)$', views2.new, name='new'),
    url(r'^create/$', views2.create, name='create'),
    url(r'^edit/(?P<edit_type>[dl]?)$', views2.edit, name='edit'),
    url(r'^update/(?P<update_type>[dl]?)$', views2.update, name='update'),
]