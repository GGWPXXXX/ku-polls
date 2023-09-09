from django.test import TestCase
import datetime
from django.urls import reverse
from django.utils import timezone
from .models import Question

class QuestionModelTests(TestCase):
    """
    Tests for the Question model.
    """

    def test_was_published_recently_with_future_question(self):
        """
        Test for the was_published_recently method with a future question.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        Test for the was_published_recently method with an old question.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        Test for the was_published_recently method with a recent question.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
    
    def test_is_published_future_pub_date(self):
        """
        Test for a question with a future pub date.
        The is_published method should return False.
        """
        future_pub_date = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=future_pub_date)
        self.assertFalse(question.is_published())

    def test_is_published_default_pub_date(self):
        """
        Test for a question with the default pub date (now).
        The is_published method should return True.
        """
        current_time = timezone.now()
        question = Question(pub_date=current_time)
        self.assertTrue(question.is_published())

    def test_is_published_past_pub_date(self):
        """
        Test for a question with a pub date in the past.
        The is_published method should return True.
        """
        past_pub_date = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=past_pub_date)
        self.assertTrue(question.is_published())
        
    def test_can_vote_with_no_end_date(self):
        """
        Test if a user can vote when there is no end_date set.
        The can_vote method should return True.
        """
        question = Question(pub_date=timezone.now())
        self.assertTrue(question.can_vote())

    def test_can_vote_before_end_date(self):
        """
        Test if a user can vote before the end_date.
        The can_vote method should return True.
        """
        future_end_date = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=timezone.now(), end_date=future_end_date)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        Test if a user cannot vote after the end_date has passed.
        The can_vote method should return False.
        """
        past_end_date = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=timezone.now(), end_date=past_end_date)
        self.assertFalse(question.can_vote())
        
    def test_cannot_vote_with_same_end_date(self):
        """
        Test if a user cannot vote when the end_date is the same as the pub_date.
        The can_vote method should return True.
        """
        current_time = timezone.now()
        question = Question(pub_date=current_time, end_date=current_time)
        self.assertTrue(question.can_vote())
    
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

class QuestionIndexViewTests(TestCase):
    """
    Tests for the Question index view.
    """
    
    def test_no_questions(self):
        """
        Test when there are no questions.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Test when there is a past question.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Test when there is a future question.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Test when there are both future and past questions.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        Test when there are two past questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    """
    Tests for the Question detail view.
    """
    
    def test_future_question(self):
        """
        Test when attempting to access a future question.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Test when accessing a past question.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
