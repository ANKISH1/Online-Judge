from django.urls import path
from compiler.views import submit

urlpatterns = [
    path("", submit, name="submit"),
]