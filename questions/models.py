from __future__ import unicode_literals

from django.db import models
from persol_users.models import PersolUser

class Question(models.Model):
    questionnaire_title = models.CharField(max_length=200)
    question_text = models.TextField(max_length=500)
    
    def get_users(self):
        persol_user_ids = Answer.objects.values("persol_user").filter(question = self).distinct()
        return PersolUser.objects.filter(id__in = persol_user_ids)

    def get_answer(self,u_id,c_id):
        answerCount = Answer.objects.filter(question = self,persol_user = u_id,choice = c_id).count()
        if answerCount == 0:
            return "-"
        return Answer.objects.filter(question = self,persol_user = u_id,choice = c_id)[0].answer_text
        
    def get_user_answers(self):
        user_answers_dict = []
        choice_answer_dict = []
        for persol_user in self.get_users():
            for choice in self.choice_set.all:
                if (self.get_answer(persol_user,choice) is None):
                    continue
                choice_answer_dict[choice.choice_text] = self.get_answer(persol_user,choice) 
            user_answers_dict[persol_user] = choice_answer_dict
        return user_answers_dict

                
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)


class Answer(models.Model):
    persol_user = models.ForeignKey(PersolUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    
    class Meta:
        unique_together=(("persol_user","question","choice"))