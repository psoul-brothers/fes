from django.conf.urls import url

from . import views

app_name = 'questions'
urlpatterns = [
    # ex: /questions/
    url(r'^$', views.index, name='index'),
    # ex: /questions/create
    url(r'^create/$', views.create, name='create'),
    # ex: /questions/registration
    url(r'^registration/$', views.registration, name='registration'),
    # ex: /questions/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /questions/5/answer
    url(r'^(?P<question_id>[0-9]+)/answer/$', views.answer, name='answer'),
    # ex: /questions/answerRegistration
    url(r'^(?P<question_id>[0-9]+)/answerRegistration/$', views.answerRegistration, name='answerRegistration'),
    # ex: /questions/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /questions/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]