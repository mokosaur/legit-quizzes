from django.contrib import admin
from .models import Label, Choice, Quiz, Question, Answer, Submit

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)

admin.site.register(Label)
admin.site.register(Submit)
admin.site.register(Choice)