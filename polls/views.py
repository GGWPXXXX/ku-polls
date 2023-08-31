from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.shortcuts import render
from django.template import loader
from .models import Question

def detail(request:HttpRequest, question_id)->HttpResponse:
    return HttpResponse("You're looking at question %s." % question_id)

def results(request:HttpRequest, question_id)->HttpResponse:
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request:HttpRequest, question_id)->HttpResponse:
    return HttpResponse("You're voting on question %s." % question_id)

def index(request:HttpRequest) -> render:
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "index.html", context)