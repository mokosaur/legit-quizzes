from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Quiz(models.Model):
    title = models.CharField(max_length=256, primary_key=True)
    type = models.CharField(max_length=64)
    logged = models.BooleanField()
    creation_date = models.DateTimeField()
    author = models.ForeignKey(User, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=256)
    type = models.CharField(max_length=64)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=256)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Label(models.Model):
    label = models.IntegerField()
    name = models.CharField(max_length=256)
    quiz = models.ForeignKey(Quiz, null=True)

    def __str__(self):
        return str(self.label)


class Submit(models.Model):
    user = models.ForeignKey(User, null=True)
    quiz = models.ForeignKey(Quiz, null=True)
    label = models.ForeignKey(Label, null=True)


class Choice(models.Model):
    submit = models.ForeignKey(Submit, null=True)
    answer = models.ForeignKey(Answer, null=True)
