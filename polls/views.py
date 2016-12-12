from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import User, Poll, Question, Answer


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'top_polls'

    def get_queryset(self):
        return sorted(Poll.objects.all(), key=lambda a: a.users_watched_results.count())[-5:]


@login_required
def poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    context = {'poll':poll}
    return render(request, 'polls/poll.html', context)


class PollResultsView(LoginRequiredMixin, generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        self.object.users_watched_results.add(self.request.user)
        context = super(PollResultsView, self).get_context_data(**kwargs)
        context['answer_list']= []
        for question in self.object.question_set.all():
            context['answer_list'].append(question.answer_set.all())
        context['answer_list'].reverse()
        context['selected_answers'] = Answer.objects.filter(question__poll=self.object, users__pk=self.request.user.pk)
        return context


@login_required
def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user,'poll_list': Poll.objects.filter(user=user.id)}
    return render(request, 'polls/profile.html', context)


@login_required
def profile(request):
    user = request.user
    context = {'poll_list': Poll.objects.filter(user=user.id)}
    return render(request, 'polls/profile.html', context)


@login_required
def question(request, poll_id, question_id):
    question = get_object_or_404(Question, pk=question_id, poll=poll_id)
    answers=question.answer_set.filter(users__pk=request.user.pk)
    if not answers:
        context = {'question':question}
        return render(request, 'polls/question.html', context)
    question_list = question.poll.question_set.all()
    for qq in question_list:
        ans = qq.answer_set.filter(users__pk=request.user.id)
        if not ans:
            return HttpResponseRedirect(reverse('polls:question', args=(poll_id, qq.id,)))
    return HttpResponseRedirect(reverse('polls:poll_results', args=(poll_id,)))


@login_required
def vote(request, poll_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_answer = question.answer_set.get(pk=request.POST['choice'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        context = { 'question': question, 'error_message': "You didn't select a choice.", }
        return render(request, 'polls/question.html', context)
    else:
        selected_answer.users.add(request.user)
        selected_answer.save()
    return HttpResponseRedirect(reverse('polls:question', args=(poll_id, question.id,)))


class UserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/user_list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        answer = get_object_or_404(Answer, pk=self.kwargs['answer_id'])
        return answer.users.all()