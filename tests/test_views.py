from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from condottieri_profiles.views import *

class CondottieriProfileViewsTests(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		self.user_0 = User.objects.create(
			username="user_0"
			)
		self.user_1 = User.objects.create(
			username="user_1"
			)

	def test_own_profile(self):
		request = self.factory.get(
			reverse('profile_detail', args=['user_0'])
		)
		request.user = self.user_0
		response = ProfileDetailView.as_view()(request, slug='user_0')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context_data['is_own'])
		request.user = self.user_1
		response = ProfileDetailView.as_view()(request, slug='user_0')
		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.context_data['is_own'])

	def test_profile_update(self):
		form_data = {
			'name': 'John Doe',
			'about': '',
			'location': 'Albacete',
			'website': 'http://condottierigame.net',
			'autosubscribe': False,
			'spokenlanguage_set-TOTAL_FORMS': 1,
			'spokenlanguage_set-INITIAL_FORMS': 0,
		}
		request = self.factory.post(reverse('profile_edit'), data=form_data)
		request.user = self.user_0
		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)
		response = ProfileUpdateView.as_view()(request)
		self.assertEqual(response.status_code, 302)


