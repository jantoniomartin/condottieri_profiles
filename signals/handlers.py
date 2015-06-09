from django.conf import settings
from django.utils.translation import ugettext_noop as _

def create_notice_types(sender, **kwargs):
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType 
        print "Creating notices for condottieri_profiles"
        NoticeType.create("karma_healed",
            _("Karma healed"),
            _("you have recovered the minimum karma to join games"))
        NoticeType.create("new_friend",
            _("New friend"),
            _("a user has befriended you"))
        NoticeType.create("friend_joined",
            _("Friend joined a game"),
            _("a friend of you has just joined a game"))
    else:
        print "condottieri_profiles: Skipping creation of NoticeTypes"
