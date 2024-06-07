from django.db import models

# Create your models here.
class submission(models.Model):
    language = models.CharField(max_length=50)
    code = models.TextField()
    input = models.TextField(null=True,blank=True)
    output = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class result(models.Model):
    language = models.CharField(max_length=50)
    code = models.TextField()
    problemId = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    