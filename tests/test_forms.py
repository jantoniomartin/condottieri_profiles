from django.test import TestCase

from condottieri_profiles import forms

class ProfileFormTestCase(TestCase):
	fixtures = []

	def test_profile_form(self):
		form = forms.ProfileForm(data={
				'name': 'John Doe',
				'about': 'I am nobody',
				'location': 'Nowhere',
				'website': 'http://example.com',
				'autosubscribe': True,
			})
		self.assertTrue(form.is_valid())


