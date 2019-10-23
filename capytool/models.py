from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Invoice(models.Model):
    """ Invoice object """
    idi = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)
    client_name = models.CharField(max_length=200)
    total_ttc = models.FloatField(default=0)
    total_tva = models.FloatField(default=0)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.idi
