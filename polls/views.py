# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from urllib2 import urlopen

from parse_files.parse_str import read_url_data, parse_for_given_groups

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
    question = get_object_or_404(Question, pk=question_pk)
    context = {
        'question': question,
    }
    return render(request, 'results.html', context)

def vote(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay question voting form with error message
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'detail.html', context)
    else:
        selected_choice.votes += 1;
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', kwargs={'question_pk': question.pk}))

def parse_url_data(request):
    url = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'
    response = read_url_data(url)
    data_dict = parse_for_given_groups(response,
        ["Very conservative","Geography","Time","Conservative, (or)", "N Size"])
    context = {
        'data_str': str(data_dict),
    }
    return render(request, 'read_url_data_view.html', context)

def parse_pollster_url_data(request):
    url = "https://elections.huffingtonpost.com/pollster/api/v2/polls?cursor=16337&sort=created_at.json"
    response = read_url_data(url)
    context = {
        'data_str': response.read().replace("\r","").replace("\n",""),
    }
    return render(request, 'read_url_data_view.html', context)
