from django.db import models

# Create your models here.


class problem(models.Model):
    name = models.CharField(max_length=50)
    statement = models.CharField(max_length=1000)
    difficulty = models.CharField(max_length=50, default="Easy")
    
class Solution(models.Model):
    problem = models.ForeignKey(problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
class TestCase(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    problem = models.ForeignKey(problem, on_delete=models.CASCADE)   