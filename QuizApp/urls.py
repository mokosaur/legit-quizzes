from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^quiz/(?P<quiz_title>.+)$', views.quiz, name='quiz'),
    url(r'^results/(?P<quiz_title>.+)$', views.results, name='results'),
    url(r'^clustering/(?P<quiz_title>.+)$', views.clustering, name='clustering'),
    url(r'^$', views.show_quizzes, name='show_quizzes'),
    url(r'^create-quiz/$', views.create_quiz, name='createquiz')
]