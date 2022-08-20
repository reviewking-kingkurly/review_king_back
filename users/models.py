from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel): 
    name     = models.CharField(max_length=45)
    email    = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=150)

    class Meta: 
        db_table = "users"