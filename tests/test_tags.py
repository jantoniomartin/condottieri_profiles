from django.test import TestCase

import condottieri_profiles.templatetags.condottieri_profiles_tags as tags

class TagsTests(TestCase):

    def test_karma_stars_0(self):
        r = tags.karma_stars(0)
        self.assertIn("0 stars", r)

    def test_score_stars_0(self):
        r = tags.score_stars(0)
        self.assertIn("0 stars", r)

