from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    # url for: /polls/
    url(r'^$', views.index, name='index'),
    # url for: /polls/<int:pk>/
    url(r'^(?P<question_pk>[0-9]+)/$', views.detail, name='detail'),
    # url for: /polls/<int:pk>/results/
    url(r'^(?P<question_pk>[0-9]+)/results/$', views.results, name='results'),
    # url for: /polls/<int:pk>/vote/
    url(r'^(?P<question_pk>[0-9]+)/vote/$', views.vote, name='vote'),
    # url for: /polls/parse_url_data/
    url(r'^parse_url_data/$', views.parse_url_data, name='parse_url_data'),
    # url for: /polls/parse_pollster_url_data/
    url(r'^parse_pollster_url_data/$', views.parse_pollster_url_data, name='parse_pollster_url_data'),

]
