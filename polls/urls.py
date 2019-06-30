from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    # url for: /polls/
    url(r'^$', views.index, name='index'),
    # url for: /polls/questions_list/
    url(r'^questions_list/$', views.questions_list, name='questions_list'),
    # url for: /polls/questions_list/
    url(r'^questions_list/include_empty_questions/$', views.questions_list_include_empty, name='questions_list_include_empty'),
    # url for: /polls/<int:pk>/
    url(r'^(?P<question_pk>[0-9]+)/$', views.detail, name='detail'),
    # url for: /polls/<int:pk>/results/
    url(r'^(?P<question_pk>[0-9]+)/results/$', views.results, name='results'),
    # url for: /polls/<int:pk>/vote/
    url(r'^(?P<question_pk>[0-9]+)/vote/$', views.vote, name='vote'),
    # url for: /polls/load_polls/
    url(r'^load_polls/$', views.parse_data, name='load_polls'),

]
