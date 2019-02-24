from django.db import models
from django.utils.timezone import now

# Create your models here.
class snapshots(models.Model):
	snapshotID = models.CharField(max_length=8)
	created = models.DateTimeField()
	backupedPath = models.CharField(max_length=32)
	host = models.CharField(max_length=32)
	absolPath = models.ForeignKey('repositories.repositories', on_delete=models.CASCADE)
