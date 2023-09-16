import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Represents a poll question.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date and time when the question was published.
    """
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField("Date Added", default=timezone.now)
    end_date = models.DateTimeField("Date Ended", null=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the question text.

        Returns:
            str: The question text.
        """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        """
        Checks if the question was published recently.

        Returns:
            bool: True if the question was published within the last day, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Checks if the question is published.

        Returns:
            bool: True if the question is published, False otherwise.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """
        Checks if the question can be voted on.

        Returns:
            bool: True if the question can be voted on, False otherwise.
        """
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date <= now
        else:
            return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """
    Represents a choice for a poll question.

    Attributes:
        question (Question): The question to which this choice belongs.
        choice_text (str): The text of the choice.
        votes (int): The number of votes received for this choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    # votes = models.IntegerField(default=0)

    @property
    def votes(self):
        # count the votes for this choice
        return self.vote_set.count()

    def __str__(self) -> str:
        """
        Returns a string representation of the choice text.

        Returns:
            str: The choice text.
        """
        return self.choice_text


class Vote(models.Model):
    """Record  a vote of choice by user"""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Question, on_delete=models.CASCADE)

