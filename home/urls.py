from django.contrib import admin
from django.urls import path, include
from .views import question_list, submit


urlpatterns = [
    path('', question_list, name ='question-list'),
    # path('problem/<int:problem_id>/',question_detail, name= 'problem-detail'),
    path('submit/<int:problem_id>/', submit, name = 'submit'),
]