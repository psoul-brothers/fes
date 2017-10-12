#coding: utf-8
from django.shortcuts import get_list_or_404,get_object_or_404, render
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,Answer
from persol_users.models import PersolUser
from django.core.urlresolvers import reverse
from django.utils import timezone
import traceback

def create(request):
    return render(request, 'questions/create.html')

def registration(request):
    try:
        q = Question(questionnaire_title=request.POST['questionnaire_title'], question_text=request.POST['question_text'])
        q.save()
        choiceText = request.POST['choice_text']
        for choice in choiceText.splitlines():
           q.choice_set.create(choice_text=choice)
            
    except :
        response = "DBエラーにより保存できませんでした。"
        traceback.format_exc()
        return HttpResponse(response + traceback.format_exc())
    else:
        return HttpResponseRedirect(reverse('questions:index'))
        
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = []
    choices = question.get_sorted_choices()
    user_answers_dict = question.get_user_answers()
    print "view user_answers_dict 長さ:%d" % len(user_answers_dict)
    for choice_answer in user_answers_dict.values(): 
        print choice_answer
        for answer in choice_answer.values():
            print answer
    
    return render(request, 'questions/detail.html', {'question': question, 'choices': choices, 'user_answers_dict':user_answers_dict})

def index(request):
    latest_question_list = Question.objects.order_by('id')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'questions/index.html', context)
    
def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'questions/answer.html', {'question': question})
    
def answerRegistration(request, question_id):
    print request.POST.getlist('choiceId')
    question = get_object_or_404(Question, pk=question_id)
    # choices = question.choice_set.all
    # choices = get_list_or_404(Choice, pk__in=request.POST.getlist('choiceId'))
    print question
    user = request.user
    try:
        for choice in question.choice_set.all()  :
            print choice.id
            answerCount = Answer.objects.filter(persol_user=user,question_id=question_id,choice_id=choice.id).count()
            if answerCount > 0:
                print answerCount
                Answer.objects.filter(persol_user=user,question_id=question_id,choice_id=choice.id).delete()
            choice.answer_set.create(persol_user=user,question_id=question_id, answer_text=request.POST['answer_text_%d' %choice.id])
        # question.answer_set.create(answer_text=request.POST['answer_text'])
    except :
        response = "DBエラーにより保存できませんでした。"
        traceback.format_exc()
        return HttpResponse(response + traceback.format_exc())
    else:
        return HttpResponseRedirect(reverse('questions:detail', args=(question.id,)))    