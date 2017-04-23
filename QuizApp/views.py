from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from django.template.context_processors import csrf
from QuizApp.models import *
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('register.html', token)


def quiz(request, quiz_title):
    if request.method == 'POST':
        form = request.POST
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        for question in form:
            if question != 'csrfmiddlewaretoken':
                answer = Answer.objects.get(pk=form[question])
                Submit(answer=answer, user=user).save()
    if Quiz.objects.filter(pk=quiz_title).exists():
        quiz = Quiz.objects.get(pk=quiz_title)
        return render(request, 'quiz.html', {'quiz': quiz})
    else:
        return render(request, 'quiz.html')


def show_quizzes(request):
    return render(request, 'show_quizzes.html', {'quizzes': Quiz.objects.all()})


def results(request, quiz_title):
    if Quiz.objects.filter(pk=quiz_title).exists():
        quiz = Quiz.objects.get(pk=quiz_title)
        return render(request, 'results.html', {'quiz': quiz})
    else:
        return render(request, 'results.html')


def create_quiz(request):
    if request.method == 'POST':
        form = request.POST
        quiz_name = form['title']
        quiz_type = form['type']
        quiz_logged = 'logged-only' in form
        questions = []
        q_number = 1
        while 'question-{}-title'.format(q_number) in form:
            question = form['question-{}-title'.format(q_number)]
            question_type = form['question-{}-type'.format(q_number)]
            answers = []
            a_number = 1
            while 'answer-{}-{}-title'.format(q_number, a_number) in form:
                answers.append(form['answer-{}-{}-title'.format(q_number, a_number)])
                a_number += 1
            questions.append((question, question_type, answers))
            q_number += 1
        quiz = Quiz(title=quiz_name, type=quiz_type, logged=quiz_logged, creation_date=timezone.now())
        quiz.save()
        for q in questions:
            question = Question(text=q[0], type=q[1], quiz=quiz)
            question.save()
            for a in q[2]:
                Answer(text=a, question=question).save()
    return render(request, 'create_quiz.html')
