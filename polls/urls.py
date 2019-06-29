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
    # url for: /polls/political_leanings/
    url(r'^political_leanings/$', views.parse_pol_lean_data, name='parse_pol_lean_data'),
    # url for: /polls/pollster/
    url(r'^pollster/$', views.parse_pollster_data, name='parse_pollster_data'),

]
