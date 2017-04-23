from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=256, primary_key=True)
    type = models.CharField(max_length=64)
    logged = models.BooleanField()
    creation_date = models.DateTimeField()

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


class Submit(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True)
