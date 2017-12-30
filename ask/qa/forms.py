from django import forms

from qa import models
from django.contrib.auth.models import User


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea())

    def clean(self):
        return self.cleaned_data

    def save(self):
        q = models.Question()
        q.author = User.objects.all()[0]
        q.text = self.cleaned_data['text']
        q.title = self.cleaned_data['title']

        q.save()
        return q


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())
    question = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
        return self.cleaned_data

    def save(self):
        ans = models.Answer()
        ans.author = User.objects.all()[0]
        ans.text = self.cleaned_data['text']
        ans.question_id = self.cleaned_data['question']

        ans.save()
        return ans
