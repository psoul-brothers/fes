from __future__ import unicode_literals

from django.db import models
from persol_users.models import PersolUser

class Question(models.Model):
    questionnaire_title = models.CharField(max_length=200)
    question_text = models.TextField(max_length=500)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

class Answer(models.Model):
    persol_user = models.ForeignKey(PersolUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)