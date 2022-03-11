from django.db import models
class Diabetes(models.Model):
    file=models.FileField()
    No_of_Neighbours = models.TextField()

# Create your models here.
