from django.test import TestCase, override_settings
from django.contrib.auth.models import User

from condottieri_profiles.models import CondottieriProfile, add_overthrow, add_surrender
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

    def test_basic_properties(self):
        user_0 = User.objects.get(username="user_0")
        profile = user_0.profile
        self.assertEqual(profile.get_absolute_url(),
                '/profiles/profile/user_0')
        self.assertEqual(str(profile), "user_0")
        self.assertEqual(profile.language, "en")
        self.assertEqual(profile.get_display_name(), "user_0")

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

    def test_check_karma_to_join_too_low(self):
        user_0 = User.objects.get(username="user_0")
        user_0.profile.adjust_karma(-100)
        msg = user_0.profile.check_karma_to_join()
        self.assertNotEqual(msg, "")
        
    def test_check_karma_to_join_too_low_for_fast(self):
        user_0 = User.objects.get(username="user_0")
        msg = user_0.profile.check_karma_to_join(fast=True)
        self.assertNotEqual(msg, "")

    def test_check_karma_to_join_too_low_for_private(self):
        user_0 = User.objects.get(username="user_0")
        msg = user_0.profile.check_karma_to_join(private=True)
        self.assertNotEqual(msg, "")

    @override_settings(GAMES_LIMIT = 0)
    def test_karma_to_unlimited_too_low(self):
        user_0 = User.objects.get(username="user_0")
        msg = user_0.profile.check_karma_to_join()
        self.assertNotEqual(msg, "")

    def test_check_karma_to_join_ok(self):
        user_0 = User.objects.get(username="user_0")
        user_0.profile.adjust_karma(100)
        msg = user_0.profile.check_karma_to_join(fast=True, private=True)
        self.assertEqual(msg, "")
    
    def test_hall_of_fame_is_zero(self):
        hof = CondottieriProfile.objects.hall_of_fame()
        self.assertEqual(hof.count(), 0)

    def test_get_time_zone_without_time_zone(self):
        user_0 = User.objects.get(username="user_0")
        offset = user_0.profile.time_zone
        self.assertEqual(offset, 0)

    def test_get_time_zone_with_time_zone(self):
        user_0 = User.objects.get(username="user_0")
        user_0.account.timezone = 'UTC'
        user_0.account.save()
        offset = user_0.profile.time_zone
        self.assertEqual(offset, 0)

    def test_add_overthrow(self):
        user_0 = User.objects.get(username="user_0")
        class DummyRevolution:
            pass
        sender = DummyRevolution()
        sender.government = user_0
        sender.voluntary = False
        self.assertIsNone(add_overthrow(sender))

    def test_add_surrender(self):
        class DummyPlayer:
            pass
        sender = DummyPlayer()
        sender.user = User.objects.get(username="user_0")
        add_surrender(sender)

    def test_create_profile(self):
        user_2 = User.objects.create(username="user_2")
        self.assertIsInstance(user_2.profile, CondottieriProfile)

    def test_adjust_karma_not_int(self):
        user_0 = User.objects.get(username="user_0")
        r = user_0.profile.adjust_karma('')
        self.assertIsNone(r)

