from django import forms

from qa import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea())

    def clean(self):
        return self.cleaned_data

    def save(self):
        q = models.Question()
        q.author = self._user
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
        ans.author = self._user
        ans.text = self.cleaned_data['text']
        ans.question_id = self.cleaned_data['question']

        ans.save()
        return ans


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def login(self):
        user = authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'])

        return user


class SignupForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean(self):
        if len(self.cleaned_data['username']) == 0:
            raise forms.ValidationError('Too short username')
        if len(self.cleaned_data['password']) == 0:
            raise forms.ValidationError('Too short password')
        if len(self.cleaned_data['email']) == 0:
            raise forms.ValidationError('Too short email')

        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('User with this email exists')

        if User.objects.filter(email=self.cleaned_data['username']).exists():
            raise forms.ValidationError('User with this username exists')

        return self.cleaned_data

    def save(self):
        params = {
            'username': self.cleaned_data['username'],
            'password': self.cleaned_data['password'],
            'email': self.cleaned_data['email']
        }
        user = User.objects.create_user(**params)
        return user
