from django.test import TestCase

# Create your tests here.
class FormTest(TestCase):
	def testForms(self):
		response = self.client.get("/snapshots/.var.backup.serverNo1/")