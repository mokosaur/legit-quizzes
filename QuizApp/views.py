from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from django.template.context_processors import csrf
from QuizApp.models import *
from django.utils import timezone
from django.core.mail import send_mail

import numpy as np
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import json


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
    quiz = Quiz.objects.get(pk=quiz_title)
    if request.method == 'POST':
        form = request.POST
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        submit = Submit(quiz=quiz, user=user)
        submit.save()
        for question in form:
            if question != 'csrfmiddlewaretoken':
                answer = Answer.objects.get(pk=form[question])
                Choice(answer=answer, submit=submit).save()

        if quiz.type == 'prediction':
            ids = []
            questions = quiz.question_set.all()
            for q in questions:
                answers = q.answer_set.all()
                ids += [a.id for a in answers]

            submits = Submit.objects.filter(quiz=quiz, label__isnull=False).all()
            X = np.zeros((len(submits), len(ids)))
            y = np.zeros(len(submits))
            for i, s in enumerate(submits):
                for c in s.choice_set.all():
                    X[i, ids.index(c.answer.id)] = 1
                y[i] = s.label.label

            knn = KNeighborsClassifier(n_neighbors=3)
            knn.fit(X, y)

            x_predict = np.zeros(len(ids))
            for c in submit.choice_set.all():
                X[ids.index(c.answer.id)] = 1

            y_predict = int(knn.predict([x_predict])[0])
            class_name = Label.objects.get(quiz=quiz, label=y_predict).name

            try:
                send_mail(
                    'Quiz results',
                    'You have been assigned to the class: {}.'.format(class_name),
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
            except:
                print("There is no SMTP client available.")

            return render(request, 'error.html', {'title': 'Your result:',
                                                  'text': 'You are classified as {}'.format(class_name),
                                                  'next': '/'})
    if Quiz.objects.filter(pk=quiz_title).exists():
        # quiz = Quiz.objects.get(pk=quiz_title)
        if quiz.logged and not request.user.is_authenticated():
            return render(request, 'error.html', {'title': 'Error!', 'text': 'You must be logged in.', 'next': '/'})
        else:
            return render(request, 'quiz.html', {'quiz': quiz})
    else:
        return render(request, 'quiz.html')


def show_quizzes(request):
    return render(request, 'show_quizzes.html', {'quizzes': Quiz.objects.all()})


def results(request, quiz_title):
    if Quiz.objects.filter(pk=quiz_title).exists():
        quiz = Quiz.objects.get(pk=quiz_title)
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        if user == quiz.author or quiz.author is None:
            print(quiz.submit_set.all())

            # Get all answers id
            ids = []
            questions = quiz.question_set.all()
            for q in questions:
                answers = q.answer_set.all()
                ids += [a.id for a in answers]

            submits = quiz.submit_set.all()
            X = np.zeros((len(submits), len(ids)))
            for i, s in enumerate(submits):
                for c in s.choice_set.all():
                    print(i, ids.index(c.answer.id))
                    X[i, ids.index(c.answer.id)] = 1

            print(X)

            Z = linkage(X, 'ward')
            labels = np.zeros((9, X.shape[0]))
            for i in range(9):
                labels[i, :] = fcluster(Z, i + 2, criterion='maxclust')
            print(labels)

            pca = PCA(2)
            X = pca.fit_transform(X)
            print(X)

            # sub_dict = {}
            data = []
            for i, row in enumerate(X):
                data.append({
                    'id': submits[i].id,
                    'x': row[0],
                    'y': row[1],
                    'name': '<br>'.join([c.answer.text for c in submits[i].choice_set.order_by('answer').all()]),
                    'label': list(labels[:, i])
                })

            return render(request, 'results.html', {'quiz': quiz, 'submits': data})
        else:
            return render(request, 'error.html', {'title': 'Error!', 'text': 'You\'re not allowed here.', 'next': '/'})
    else:
        return render(request, 'results.html')


def clustering(request, quiz_title):
    if Quiz.objects.filter(pk=quiz_title).exists():
        quiz = Quiz.objects.get(pk=quiz_title)
        print(request.POST)
        data = json.loads(request.POST['json'])

        for d in data:
            id = d['id']
            label = d['label']
            submit = Submit.objects.get(pk=id)
            if Label.objects.filter(quiz=quiz, label=label).exists():
                label_instance = Label.objects.get(quiz=quiz, label=label)
            else:
                label_instance = Label(quiz=quiz, label=label, name=label)
                label_instance.save()
            submit.label = label_instance
            submit.save()
        quiz.type = 'prediction'
        quiz.save()
    return HttpResponse('ok')


def create_quiz(request):
    if request.method == 'POST':
        form = request.POST
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        quiz_name = form['title']
        # quiz_type = form['type']
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
        quiz = Quiz(title=quiz_name, type='aquisition', logged=quiz_logged, creation_date=timezone.now(), author=user)
        quiz.save()
        for q in questions:
            question = Question(text=q[0], type=q[1], quiz=quiz)
            question.save()
            for a in q[2]:
                Answer(text=a, question=question).save()
        return render(request, 'error.html',
                      {'title': 'Thank you!', 'text': 'Your quiz has been successfully created.', 'next': '/'})

    return render(request, 'create_quiz.html')
