"""pub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include,url
from django.contrib import admin

from django.conf import settings
from django.views import static

import events.views

urlpatterns = [
    url(r'^$', events.views.event_index, name='portal'),
    url(r'^log', include('my_auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^events/(?P<event_id>[0-9]+)/comments/', include('comments.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^persol_users/', include('persol_users.urls')),
    url(r'^questions/', include('questions.urls')),
    # for access to uploaded files
    url(r'^files/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
]
