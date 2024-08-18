from django.contrib import admin
from django.urls import path, include
from .views import question_list, question_detail


urlpatterns = [
    path('', question_list, name ='question-list'),
    path('problem/<int:problem_id>/',question_detail, name= 'problem-detail'),
]