from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.utils import timezone
from django.views import generic

class IndexView(generic.ListView):
    """
    View for displaying the index page with the latest questions.
    """
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last 5 public questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class ResultsView(generic.DetailView):
    """
    View for displaying the results of a specific question.
    """
    model = Question
    template_name = "results.html"

class DetailView(generic.DetailView):
    """
    View for displaying the details of a specific question.
    """
    model = Question
    template_name = "detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
    """
    View for handling the voting process for a specific question.
    """
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
