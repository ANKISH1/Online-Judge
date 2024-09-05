from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import question_list, submit, leaderboard, post_logout


urlpatterns = [
    path('', question_list, name ='question_list'),
    # path('problem/<int:problem_id>/',question_detail, name= 'problem-detail'),
    path('submit/<int:problem_id>/', submit, name = 'submit'),
    path('leaderboard/', leaderboard, name = 'leaderboard'),
    path('logout/', post_logout, name='logout'),
    # path('post-logout/', post_logout, name='post_logout'),

]