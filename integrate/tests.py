from django.test import TestCase
from .forms import integrateInformation

# Create your tests here.
class FormTest(TestCase):
	def testForms(self):
		formData = {
			'user':'zoerbdo',
			'password':'AdminAdmin',
			'dest':'zoerb.ccd',
			'repoPath':'/var/backup/',
			'backupPath':'/etc/'
			}
		form = integrateInformation(data=formData)
		self.assertTrue(form.is_valid())
