from django.db import models

# Create your models here.
class repositories(models.Model):
	name = models.CharField(max_length=16)
	absolPath = models.CharField(max_length=32, primary_key=True)
	diskSpace = models.CharField(max_length=8)
	lastUpdate = models.DateField()
	health = models.IntegerField()
