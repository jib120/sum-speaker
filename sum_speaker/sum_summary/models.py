from django.db import models
from datetime import datetime

# Create your models here.
class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.TextField(max_length=50)
    password = models.CharField(max_length=50)
    reg_date = models.DateTimeField(default=datetime.now(), blank=True)
    update_date = models.DateTimeField(default=datetime.now(), blank=True)

class Candidate(models.Model):
    name = models.CharField(max_length=10)
    introduction = models.TextField()
    area = models.CharField(max_length=15)
    party_number = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=20)
    summary = models.TextField()
    reg_date = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.keyword

class Images(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    reg_date = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.Images