from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Problem
from django.template import loader
from django.http import HttpResponse



# Create your views here.
@login_required
def question_list(request):
    all_questions = Problem.objects.all()
    context = {
        'all_questions':all_questions
    }
    template = loader.get_template('all_questions.html')
    return HttpResponse(template.render(context,request))

def question_detail(request, problem_id):
    question= get_object_or_404(Problem, id = problem_id)
    context = {
        'question':question
    }
    template = loader.get_template('question_detail.html')
    return HttpResponse(template.render(context, request))




