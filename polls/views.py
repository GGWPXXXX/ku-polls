from django.http import Http404, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Question, Choice, Vote
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


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
        user_vote_id = get_selected_choice(request.user, self.object)
        context = self.get_context_data(
            object=self.object, user_vote_id=user_vote_id)
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

    user = request.user
    try:
        vote = Vote.objects.get(user=user, choice__question=question)
        # update this vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        vote = Vote(user=user, choice=selected_choice)
    vote.save()

    return redirect("polls:results", question.id)


class LogoutView(LogoutView):
    """Summary

    Args:
        LogoutView (TYPE): Description
    """
    next_page = reverse_lazy('polls:index')


def signup(request: HttpRequest):
    """ signup for a new user account 

    Args:
        request (HttpRequest): 

    Returns:
        TYPE: Description
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def get_selected_choice(user, question):
    """ get the selected choice for a user. """
    # Check if the user is logged in
    if user.is_authenticated:
        try:
            vote = Vote.objects.get(user=user, choice__question=question)
            selected_choice_id = vote.choice.id
        except Vote.DoesNotExist:
            selected_choice_id = None
    else:
        selected_choice_id = None  # User is not logged in

    return selected_choice_id
