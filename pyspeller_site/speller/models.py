from django.db import models

class Addwords(models.Model):
    word = models.CharField(max_length=50)
