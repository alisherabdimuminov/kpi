from uuid import uuid4
from django.db import models

from users.models import User


class Question(models.Model):
    question = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()
    correct = models.CharField(max_length=100)
    point = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.question


class Test(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, related_name="test_questions")
    passed_score = models.DecimalField(max_digits=10, decimal_places=2)
    
