from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^polls/(?P<poll_id>[0-9]+)/$', views.poll, name='poll'),
    url(r'^polls/(?P<poll_id>[0-9]+)/questions/(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'^polls/(?P<pk>[0-9]+)/results/$', views.PollResultsView.as_view(), name='poll_results'),
    url(r'^polls/(?P<poll_id>[0-9]+)/questions/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^users/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^polls/(?P<poll_id>[0-9]+)/questions/(?P<question_id>[0-9]+)/answers/(?P<answer_id>[0-9]+)/$',
        views.UserListView.as_view(), name='user_list'),
    url(r'^polls/new/$', views.PollCreate.as_view(), name='poll_create'),
    url(r'^polls/(?P<poll_id>[0-9]+)/questions/new$', views.QuestionCreate.as_view(), name='question_create'),
    url(r'^polls/(?P<poll_id>[0-9]+)/questions/(?P<question_id>[0-9]+)/add_answer$',
        views.AnswerCreate.as_view(), name='answer_create'),
]