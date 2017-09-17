#coding: utf-8
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,Answer
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
            c = q.choice_set.create(choice_text=choice)        
    except :
        response = "DBエラーにより保存できませんでした。"
        traceback.format_exc()
        return HttpResponse(response + traceback.format_exc())
    else:
        return HttpResponseRedirect(reverse('questions:index'))
        
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'questions/detail.html', {'question': question})

def index(request):
    latest_question_list = Question.objects.order_by('id')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'questions/index.html', context)
    
def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'questions/answer.html', {'question': question})
    
def answerRegistration(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        question.answer_set.create(answer_text=request.POST['answer_text'])
    except :
        response = "DBエラーにより保存できませんでした。"
        traceback.format_exc()
        return HttpResponse(response + traceback.format_exc())
    else:
        return HttpResponseRedirect(reverse('questions:detail', args=(question.id,)))    