# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from persol_users.models import PersolUser
from collections import OrderedDict

class Question(models.Model):
    questionnaire_title = models.CharField(max_length=200)
    question_text = models.TextField(max_length=500)
    
    def get_users(self):
        persol_user_ids = Answer.objects.values("persol_user").filter(question = self).distinct()
        return PersolUser.objects.filter(id__in = persol_user_ids)

    def get_sorted_choices(self):
        choices = []
        for choice in self.choice_set.all().order_by('id'):
            choices.append(choice.choice_text)
        return choices

    def get_answer(self,u_id,c_id):
        answerCount = Answer.objects.filter(question = self,persol_user = u_id,choice = c_id).count()
        if answerCount == 0:
            return "-"
        return Answer.objects.filter(question = self,persol_user = u_id,choice = c_id)[0].answer_text
        
    def get_user_answers(self):
        user_answers_dict = {}
        choice_answer_dict = {}
        choices = self.choice_set.all()
        for persol_user in self.get_users():
            print "models"
            print choices
            for i,choice in enumerate(choices):
                print choice.choice_text
                choice_answer_dict[i] = self.get_answer(persol_user,choice) 
            user_answers_dict[persol_user] = OrderedDict(sorted(choice_answer_dict.items(), key=lambda x: x[0]))
        return user_answers_dict
    
    # 
    def get_choices_text(self):
        return '\n'.join(self.choice_set.values_list('choice_text', flat=True))
        
    # 選択肢を設定
    def set_choices(self, choices_text):
        # 今回の文字列にない選択肢は削除
        for ch in self.choice_set.all():
            if ch.choice_text not in choices_text.splitlines():
                ch.delete()
        
        # 今回の文字列で選択し追加･更新
        for text in choices_text.splitlines():
            c = self.choice_set.filter(choice_text=text).first()
            if c is None:
                self.choice_set.create(choice_text=text)
            else:
                c.choice_text = text
                c.save()
        

                
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