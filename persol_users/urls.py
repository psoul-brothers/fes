from django.conf.urls import url

from . import views

app_name = 'persol_users'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^user_add/$', views.user_add, name='user_add'),
    url(r'^user_add_operation/$', views.user_add_operation, name='user_add_operation'),
]