# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from urllib2 import urlopen
from django.utils import timezone
import json
import os

from parse_files.parse_str import read_url_data, parse_for_pol_lean_groups, parse_for_ny_data, parse_for_datetime

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

    question = get_object_or_404(Question, pk=question_pk)
    context = {
        'question': question,
    }
    return render(request, 'detail.html', context);

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
        return render(request, 'detail.html', context)
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

def parse_ny_data(request):
    """ Reads data from url, parses data, and converts data into Question
        and Choices. """

    # read data from url
    url = 'https://bbotllc.github.io/candidate-interviews/political_leanings.json'
    response = read_url_data(url)
    entries = parse_for_ny_data(response)

    # generate data for development use
    context = {
        'data_str': str(entries),
    }

    # choices to parse for
    choices = ["Very conservative","Conservative, (or)",
        "Moderate","Liberal, (or)", "Very liberal"]

    # add entry to database
    for entry in entries:
        question = Question.objects.get_or_create(
            question_text = 'What was your political leaning in {}?'.format(entry["Time"]) ,
            pub_date = timezone.now(),
            slug = 'New_York' + str(entry["Time"])
        )[0]

        # convert N Size string to an int
        num_voters = int(entry["N Size"].replace(",",""))
        # track sum of decided voders, use to calculate proper # of undecided
        num_decided_voters = 0

        for choice in choices:
            vote_percent = entry[choice]
            num_votes = int(vote_percent*num_voters)
            Choice.objects.get_or_create(
                question = question,
                choice_text = choice,
                votes = num_votes,
            )
            num_decided_voters += num_votes

        # calculate number of undecided voters and add to database
        Choice.objects.get_or_create(
            question = question,
            choice_text = "Undecided",
            votes = num_voters - num_decided_voters,
        )

    return render(request, 'read_url_data_view.html', context)


def parse_pollster_data(request):
    """ Reads data from url, parses data, and converts data into Question
        and Choices. """

    url = "https://elections.huffingtonpost.com/pollster/api/v2/polls?cursor=16337&sort=created_at.json"

    rel_url = "parse_files/response_1561758504952.json"
    abs_url = os.path.abspath(rel_url)
    url = "file://" + abs_url

    response = read_url_data(url)

    data = json.loads(response.read())
    context = {
        'data_str': str(data),
    }

    poll_entries = data["items"]

    for poll_entry in poll_entries:

        # get slug
        slug = poll_entry["slug"]

        # extract questions
        poll_questions = poll_entry["poll_questions"]

        # for each question, save the question and results
        for question_info in poll_questions:
            question = Question.objects.get_or_create(
                question_text = question_info["text"],
                pub_date = parse_for_datetime(question_info["question"]["created_at"]),
                slug = slug,
            )[0]

            poll_result = question_info["sample_subpopulations"][0]

            num_voters = poll_result["observations"]
            choices_list = poll_result["responses"]

            for choice in choices_list:
                Choice.objects.get_or_create(
                    question = question,
                    choice_text = choice["text"],
                    votes = int(choice["value"]/100.0*num_voters),
                )


    return render(request, 'read_url_data_view.html', context)
