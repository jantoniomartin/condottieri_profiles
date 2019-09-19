from django.test import TestCase
from django.contrib.auth.models import User

from condottieri_profiles.management.commands.heal_karma import Command

class CommandTestCase(TestCase):
    
    def setUp(self):
        user_0 = User.objects.create(
            username="user_0"
            )
        user_1 = User.objects.create(
            username="user_1"
            )

    def test_handle_noargs(self):
        user_0 = User.objects.get(username="user_0")
        user_0.profile.adjust_karma(-50)
        command = Command()
        self.assertIsNone(command.handle_noargs())
