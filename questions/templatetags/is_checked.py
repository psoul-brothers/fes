# coding:utf-8
from django import template
from questions.models import Choice

register = template.Library()

@register.filter(name=u'get_answer')
def get_answer(choice_id, user_id):
	answer_text = Choice.get_answer(choice_id,user_id)
	return answer_text

@register.filter(name=u'is_checked')
def is_checked(value, arg):
	if value == arg:
		return 'checked="checked"'
	else:
		return ""

@register.filter
def answer_count(choice, answer):
	return choice.answer_set.filter(answer_text=answer).count()
