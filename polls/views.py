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
        return sorted(Poll.objects.all(), key=lambda a: a.users_watched_results.count())[-20:]


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
    user1 = get_object_or_404(User, pk=user_id)
    context = {'user1': user1,'poll_list': Poll.objects.filter(user=user1.id)}
    return render(request, 'polls/profile.html', context)


@login_required
def profile(request):
    user1 = request.user
    context = {'poll_list': Poll.objects.filter(user=user1.id), 'user1': user1}
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
        context = { 'question': question, 'error_message': "Выберите вариант"}
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


class PollCreate(generic.CreateView):
    model = Poll
    template_name = 'polls/base_form.html'
    fields = ['title']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PollCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(PollCreate, self).get_context_data(**kwargs)
        ctx['text_form'] = 'Заголовок опроса:'
        ctx['field_name'] = 'title'
        return ctx

class QuestionCreate(generic.CreateView):
    model = Question
    template_name = 'polls/base_form.html'
    fields = ['question_text']

    def form_valid(self, form):
        form.instance.poll = get_object_or_404(Poll, pk=self.kwargs['poll_id'])
        return super(QuestionCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(QuestionCreate, self).get_context_data(**kwargs)
        ctx['text_form'] = 'Текст вопроса:'
        ctx['field_name'] = 'question_text'
        return ctx

class AnswerCreate(generic.CreateView):
    model = Answer
    template_name = 'polls/base_form.html'
    fields = ['answer_text']

    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        return super(AnswerCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(AnswerCreate, self).get_context_data(**kwargs)
        ctx['text_form'] = 'Текст ответа:'
        ctx['field_name'] = 'answer_text'
        return ctx