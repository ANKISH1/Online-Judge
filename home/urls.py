from django.contrib import admin
from django.urls import path, include
from .views import question_list


urlpatterns = [
    path('', question_list, name ='question-list'),
]