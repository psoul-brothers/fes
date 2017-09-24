from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'my_auth'
urlpatterns = [
    url(r'^in/$',auth_views.login,{'template_name': 'my_auth/login.html'}, name='login'),
    url(r'^out/$',auth_views.logout,{'template_name': 'my_auth/logout.html'},name='logout'),
]