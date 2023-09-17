from django.test import TestCase
import datetime
from django.utils import timezone
from ..models import Question


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

    def test_can_vote_future_end_date(self):
        """
        Test if a user can vote when the end_date is set to a future date.
        The can_vote method should return True.
        """
        future_end_date = timezone.now(
        ) + datetime.timedelta(days=7)  # Set end_date 7 days in the future
        question = Question(pub_date=timezone.now(), end_date=future_end_date)
        self.assertTrue(question.can_vote())
