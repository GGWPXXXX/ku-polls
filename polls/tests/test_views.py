from django.test import TestCase, Client
from ..models import Question, Choice
from django.utils import timezone
from django.urls import reverse

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        now = timezone.now()
        end_date = now + timezone.timedelta(days=1)
        cls.question_1 = Question.objects.create(question_text="Who is better you or me?", pub_date=now, end_date=end_date)
        cls.choice_1 = Choice.objects.create(question=cls.question_1, choice_text="You")
        cls.choice_2 = Choice.objects.create(question=cls.question_1, choice_text="Me")
        
    def test_index_views_access(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)

        
    def test_index_views_text(self):
        response = self.client.get(reverse("polls:index"))
        words = ["Question", "Status", "Result"]
        for i in words:
            self.assertContains(response, text=i)
            
    def test_results_views_access(self):
        response = self.client.get(reverse("polls:results", args=[self.question_1.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_results_views_text(self):
        response = self.client.get(reverse("polls:results", args=[self.question_1.pk]))
        words = [self.question_1, "Vote Count", self.choice_1, self.choice_2]
        for i in words:
            self.assertContains(response,text=i)
        
        
        
        