from django.test import TestCase
from .forms import integrateInformation

# Create your tests here.
class FormTest(TestCase):
	def testForms(self):
		formData = {
			'user':'zoerbdo',
			'password':'AdminAdmin',
			'dest':'zoerb.cc',
			'repoPath':'/var/backup/repo',
			'backupPath':'/etc/'
			}
		response = self.client.post("/integrate/", formData)