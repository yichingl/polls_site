# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from django.shortcuts import render
from django.template import loader

from models import Question, Choice

def index(request):
    template = loader.get_template('index.html')

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request));

def detail(request, question_pk):
    return HttpResponse("You're looking at question %s" % question_pk)

def results(request, question_pk):
    return HttpResponse("You're looking at results of question %s" % question_pk)

def vote(request, question_pk):
    return HttpResponse("You're voting on results of question %s" % question_pk)
