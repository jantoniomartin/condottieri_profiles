from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import ObjectDoesNotExist

from condottieri_common.models import Server
from condottieri_profiles.context_processors import sidebar_ranking

class ContextProcessorsTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user_0 = User.objects.create(
            username="user_0"
            )
    
    def test_sidebar_ranking_no_server(self):
        request = self.factory.get('/')
        request.user = self.user_0
        self.assertRaises(ObjectDoesNotExist, sidebar_ranking, request)
    
    def test_sidebar_ranking(self):
        now = datetime.now()
        Server.objects.create(ranking_last_update=now)
        request = self.factory.get('/')
        request.user = self.user_0
        r = sidebar_ranking(request)
        self.assertEqual(r['ranking_last_update'], now)

    def test_sidebar_ranking_no_user(self):
        now = datetime.now()
        Server.objects.create(ranking_last_update=now)
        request = self.factory.get('/')
        request.user = AnonymousUser()
        r = sidebar_ranking(request)
        self.assertEqual(r['ranking_last_update'], now)

