from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):

    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateField()
    rating = models.IntegerField()
    author = models.ForeignKey(User)
    likes = models.ManyToManyField(User)


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)


class QuestionManager:

    @staticmethod
    def new(self):
        return Question.objects.latest('added_at')

    @staticmethod
    def popular(self):
        return Question.objects.order_by('-rating')
