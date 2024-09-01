from django.urls import path
from .views import submit


urlpatterns = [
    path("", submit, name="submit"),
    # path('problem/<int:problem_id>/',question_detail, name= 'problem-detail'),
]