from django.db import models
from django.utils import timezone

# Create your models here.
class Invoice(models.Model):
    """ Invoice object """
    idi = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    total_ttc = models.CharField(max_length=200)
    total_tva = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.idi
