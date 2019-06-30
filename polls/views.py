# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from urllib2 import urlopen
from django.utils import timezone
import json
import os

from parse_files.parse_data import read_url_data, parse_for_pol_lean_groups, parse_for_datetime
from parse_files.parse_data import parse_ny_data, parse_pollster_data

from models import Question, Choice

def index(request):
    """ Display latest 5 questions on the polls index page. """

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'index.html', context);

def detail(request, question_pk):
    """ Display a Question and all Choices to allow user to vote. """

    # question = get_object_or_404(Question, pk=question_pk)
    question = get_object_or_404(Question, pk=question_pk)
    context = {
        'question': question,
    }
    return render(request, 'detail_single.html', context);

def questions_list(request):
    """ Display all Questions and all Choices to allow user to vote. """

    questions = Question.objects.all()

    return render(request, 'detail.html', {
        'questions': questions,
    })

def results(request, question_pk):
    """ Display results of a specific question. """

    question = get_object_or_404(Question, pk=question_pk)
    context = {
        'question': question,
    }
    return render(request, 'results.html', context)

def vote(request, question_pk):
    """ Performs voting action and redirects to results page. """

    question = get_object_or_404(Question, pk=question_pk)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay question voting form with error message
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'detail_single.html', context)
    else:
        selected_choice.votes += 1;
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', kwargs={'question_pk': question.pk}))

def parse_pol_lean_data(request):
    """ Practice view to parse a list of groups from url. """

    url = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'
    response = read_url_data(url)
    data_dict = parse_for_pol_lean_groups(response,
        ["Very conservative","Geography","Time","Conservative, (or)", "N Size"])
    context = {
        'data_str': str(data_dict),
    }
    return render(request, 'read_url_data_view.html', context)

def parse_data(request):
    """ Parses data from all poll urls and saves data to database,
        then returns Http response that says 'Done'. """

    url = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'
    parse_ny_data(url)

    # start at most recent polls
    base_url = "https://elections.huffingtonpost.com/pollster/api/v2/polls?cursor={}&sort=created_at.json"
    next_cursor = 28987

    # load all 40 polls
    # num_polls = 40
    num_polls = 1
    for num_poll in range(num_polls):
        next_cursor = parse_pollster_data(base_url.format(next_cursor))

    context = {
            'data_str': "success",
        }

    return HttpResponse("success")
