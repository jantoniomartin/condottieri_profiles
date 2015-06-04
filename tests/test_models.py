from django.test import TestCase
from django.contrib.auth.models import User

from condottieri_profiles.models import CondottieriProfile
from condottieri_profiles.defaults import *

class CondottieriProfileTestCase(TestCase):
	fixtures = []

	def setUp(self):
		user_0 = User.objects.create(
			username="user_0"
			)
		user_1 = User.objects.create(
			username="user_1"
			)

	def test_get_absolute_url(self):
		user_0 = User.objects.get(username="user_0")
		profile = user_0.profile
		self.assertEqual(profile.get_absolute_url(),
				'/profiles/profile/user_0')

	def test_has_languages(self):
		user_0 = User.objects.get(username="user_0")
		user_1 = User.objects.get(username="user_1")
		user_0.profile.spokenlanguage_set.create(code='en')
		self.assertTrue(user_0.profile.has_languages())
		self.assertFalse(user_1.profile.has_languages())

	def test_average_score(self):
		user_0 = User.objects.get(username="user_0")
		prof = user_0.profile
		self.assertEqual(prof.average_score(), 0)
		prof.finished_games = 10
		prof.total_score = 5
		prof.save()
		self.assertEqual(prof.average_score(), 0.5)

	def test_adjust_karma(self):
		user_0 = User.objects.get(username="user_0")
		prof = user_0.profile
		karma = prof.karma
		prof.adjust_karma(1)
		self.assertEqual(prof.karma, karma + 1)
		prof.adjust_karma(-2)
		self.assertEqual(prof.karma, karma - 1)
		prof.adjust_karma(KARMA_MAXIMUM + 1)
		self.assertEqual(prof.karma, KARMA_MAXIMUM)
		prof.adjust_karma(-2 * KARMA_MAXIMUM)
		self.assertEqual(prof.karma, KARMA_MINIMUM)

	def test_overthrow(self):
		user_0 = User.objects.get(username="user_0")
		prof = user_0.profile
		o = prof.overthrows
		prof.overthrow()
		self.assertEqual(prof.overthrows, o + 1)

	def test_check_karma_to_join(self):
		##TODO
		pass

	def test_add_overthrow(self):
		##TODO
		pass

	def test_add_surrender(self):
		##TODO
		pass

	def test_create_profile(self):
		user_2 = User.objects.create(username="user_2")
		self.assertIsInstance(user_2.profile, CondottieriProfile)

