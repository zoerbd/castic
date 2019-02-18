from django.db import models
#from datetime import datetime
from django.utils.timezone import now

# Create your models here.
class repositories(models.Model):
	name = models.CharField(max_length=16)
	absolPath = models.CharField(max_length=32, primary_key=True)
	diskSpace = models.CharField(max_length=16)
	lastUpdate = models.DateTimeField(default=now)
	health = models.IntegerField()