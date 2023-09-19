from django.test import TestCase
from ..models import Question, Choice
from django.utils import timezone
from django.urls import reverse


class TestViews(TestCase):
    """
    Test class for testing views in the 'polls' app.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up initial data for testing views.
        Create a test question and choices.
        """
        now = timezone.now()
        end_date = now + timezone.timedelta(days=1)
        cls.question_1 = Question.objects.create(
            question_text="Who is better, you or me?", pub_date=now, end_date=end_date)
        cls.choice_1 = Choice.objects.create(
            question=cls.question_1, choice_text="You")
        cls.choice_2 = Choice.objects.create(
            question=cls.question_1, choice_text="Me")

    def test_index_views_status(self):
        """
        Test the status code of the 'index' view.
        Expected status code: 200 (OK).
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_views_text(self):
        """
        Test the content of the 'index' view.
        Check if specific words and the test question are present in the response.
        """
        response = self.client.get(reverse("polls:index"))
        words = ["Question", "Status", "Result", str(self.question_1)]
        for word in words:
            self.assertContains(response, text=word)

    def test_results_views_status(self):
        """
        Test the status code of the 'results' view.
        Expected status code: 200 (OK).
        """
        response = self.client.get(
            reverse("polls:results", args=[self.question_1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_results_views_text(self):
        """
        Test the content of the 'results' view.
        Check if the test question, "Vote Count," and choices are present in the response.
        """
        response = self.client.get(
            reverse("polls:results", args=[self.question_1.pk]))
        words = [str(self.question_1), "Vote Count",
                 str(self.choice_1), str(self.choice_2)]
        for word in words:
            self.assertContains(response, text=word)

    def test_detail_views_status(self):
        """
        Test the status code of the 'detail' view.
        Expected status code: 200 (OK).
        """
        response = self.client.get(
            reverse("polls:detail", args=[self.question_1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_views_text(self):
        """
        Test the content of the 'detail' view.
        Check if the test question and choices are present in the response.
        """
        response = self.client.get(
            reverse("polls:detail", args=[self.question_1.pk]))
        words = [str(self.question_1), str(self.choice_1), str(self.choice_2)]
        for word in words:
            self.assertContains(response, text=word)

    def test_logout_views_status(self):
        """
        Test the status code of the 'logout' view.
        Expected status code: 302 (Found/Redirect).
        """
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
