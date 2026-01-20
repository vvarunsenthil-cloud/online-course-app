from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Stores a question for an exam.
    """
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """
    Stores choices for a question.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    """
    Stores a user's submission for an exam.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(
        Choice
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.username}"
