from django.http import HttpRequest, HttpResponse, Http404
from django.urls import path
from django.shortcuts import render
from django.template import loader
from .models import Question
from django.shortcuts import get_object_or_404

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "index.html", context)

def detail(request:HttpRequest, question_id)->HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "detail.html", {"question": question})

def results(request:HttpRequest, question_id)->HttpResponse:
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request:HttpRequest, question_id)->HttpResponse:
    return HttpResponse("You're voting on question %s." % question_id)

