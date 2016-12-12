import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    users_watched_results = models.ManyToManyField(User, blank=True, related_name = 'watched_poll')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('polls:poll', args=(self.pk,))


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    #def_answer = models.BooleanField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('polls:question', args=(self.poll.id, self.pk))


class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.answer_text

    def get_absolute_url(self):
        return reverse('polls:question', args=(self.question.poll.id, self.question.id))