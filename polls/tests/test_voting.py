from django.test import TestCase
import datetime
from django.urls import reverse
from django.utils import timezone
from ..models import Choice, Question, Vote
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


def create_question(question_text, days):
    """
    Create a question with the given question_text and a publication date offset by the given number of days.

    Args:
        question_text (str): The text of the question.
        days (int): The number of days to offset the publication date.

    Returns:
        Question: The created Question object.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, choice_text):
    """
    Create a choice for a given question.

    Args:
        question (Question): The question for which the choice is created.
        choice_text (str): The text of the choice.

    Returns:
        Choice: The created Choice object.
    """
    return Choice.objects.create(question=question, choice_text=choice_text)


class QuestionDetailViewTests(TestCase):
    """
    Tests for the Question detail view.
    """

    def test_future_question(self):
        """
        Test when attempting to access a future question.
        """
        future_question = create_question(
            question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Test when accessing a past question.
        """
        past_question = create_question(
            question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


def test_vote_valid_choice(self):
    """
    Test when a user votes for a valid choice.
    """
    self.client.login(username="testuser", password="testpassword")
    question = create_question(question_text="Valid Vote Question", days=-1)
    choice = create_choice(question, "Valid Choice")
    url = reverse("polls:vote", args=(question.id,))
    response = self.client.post(url, {"choice": choice.id})
    self.assertRedirects(response, reverse(
        "polls:results", args=(question.id,)))


def test_vote_invalid_choice(self):
    """
    Test when a user votes for an invalid choice.
    """
    self.client.login(username="testuser", password="testpassword")
    question = create_question(question_text="Invalid Vote Question", days=-1)
    url = reverse("polls:vote", args=(question.id,))
    response = self.client.post(url, {"choice": 999})  # Invalid choice ID
    self.assertEqual(response.status_code, 200)
    messages = list(get_messages(response.wsgi_request))
    self.assertEqual(len(messages), 1)
    self.assertIn("You didn't select a choice.", str(messages[0]))


def test_vote_authenticated_user(self):
    """
    Test if an authenticated user can vote.
    """
    self.client.login(username="testuser", password="testpassword")
    question = create_question(question_text="Vote Question", days=-1)
    url = reverse("polls:vote", args=(question.id,))
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)


def test_vote_unauthenticated_user(self):
    """
    Test if an unauthenticated user cannot vote.
    """
    question = create_question(question_text="Vote Question", days=-1)
    url = reverse("polls:vote", args=(question.id,))
    response = self.client.get(url)
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, f"{reverse('login')}?next={url}")


def test_vote_update_existing_vote(self):
    """
    Test if an existing vote is updated when the user votes again.
    """
    user = User.objects.create_user(
        username="testuser", password="testpassword")
    self.client.login(username="testuser", password="testpassword")
    question = create_question(question_text="Update Vote Question", days=-1)
    choice1 = create_choice(question, "Choice 1")
    choice2 = create_choice(question, "Choice 2")
    vote = Vote.objects.create(user=user, choice=choice1)
    updated_vote = Vote.objects.get(pk=vote.pk)
    self.assertEqual(updated_vote.choice, choice2)


def test_vote_create_new_vote(self):
    """
    Test if a new vote is created when the user votes for the first time.
    """
    user = User.objects.create_user(
        username="testuser", password="testpassword")
    self.client.login(username="testuser", password="testpassword")
    question = create_question(question_text="New Vote Question", days=-1)
    choice = create_choice(question, "Choice")
    new_vote = Vote.objects.filter(user=user, choice=choice).first()
    self.assertIsNotNone(new_vote)
