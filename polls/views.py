# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello!  Polls index.")

def detail(request, question_pk):
    return HttpResponse("You're looking at question %s" % question_pk)

def results(request, question_pk):
    return HttpResponse("You're looking at results of question %s" % question_pk)
