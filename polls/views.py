# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404

from models import Question, Choice

def index(request):

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'index.html', context);

def detail(request, question_pk):

    question = get_object_or_404(Question, pk=question_pk)
    context = {
        'question': question,
    }
    return render(request, 'detail.html', context);

def results(request, question_pk):
    return HttpResponse("You're looking at results of question %s" % question_pk)

def vote(request, question_pk):
    return HttpResponse("You're voting on results of question %s" % question_pk)
