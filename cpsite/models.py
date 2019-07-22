from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100,default='')
    password = models.CharField(max_length=100,default='')