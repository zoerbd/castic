from django.db import models

# Create your models here.
class passwd(models.Model):
	username = models.CharField(max_length=16)
	password = models.CharField(max_length=64)
	permission = models.CharField(max_length=2)