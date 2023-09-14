from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Question, Choice, Vote
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

class IndexView(generic.ListView):
    """
    View for displaying the index page with the latest questions.
    """
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the public questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")

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

    def get(self, request, *args, **kwargs):
        """
        Get the details of a specific question.

        Args:
            request (HttpRequest): The request object.

        Raises:
            Http404: If the question is not found.

        Returns:
            HttpResponse: The response object.
        """
        self.object = self.get_object()

        # Check if the poll is votable
        if not self.object.can_vote():
            raise Http404("This poll is closed and cannot be voted on.")

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

@login_required
def vote(request, question_id):
    """
    View for handling the voting process for a specific question.
    """
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, "Voting is not allowed for this question.")
        return redirect("polls:index")

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
    # selected_choice.votes += 1
    # selected_choice.save()
    user = request.user
    try:
        vote = Vote.objects.get(user=user, choice__question=question)
        #update this vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        vote = Vote(user=user, choice=selected_choice)
    vote.save()
    
    return redirect("polls:results", question.id)

class LogoutView(LogoutView):
    next_page = reverse_lazy('polls:index')
