from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views

app_name = 'my_auth'
urlpatterns = [
    url(r'^in/$',views.login, name='login'),
    url(r'^out/$',auth_views.logout,{'template_name': 'my_auth/logout.html'},name='logout'),
]