from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Question
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Choice, Question
from django.views import generic

class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        "return the last 5 public question."
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class ResultsView(generic.DetailView):
    model = Question
    template_name = "results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
        
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

