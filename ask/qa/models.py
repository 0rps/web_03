from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):

    def new(self):
        return self.latest('added_at')

    def popular(self):
        return self.order_by('-rating')


# Create your models here.
class Question(models.Model):

    objects = QuestionManager()

    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    likes = models.ManyToManyField(User)


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')



