## Copyright (c) 2010 by Jose Antonio Martin <jantonio.martin AT gmail DOT com>
## This program is free software: you can redistribute it and/or modify it
## under the terms of the GNU Affero General Public License as published by the
## Free Software Foundation, either version 3 of the License, or (at your option
## any later version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
## FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
## for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/agpl.txt>.
##
## This license is also included in the file COPYING
##
## AUTHOR: Jose Antonio Martin <jantonio.martin AT gmail DOT com>

from datetime import datetime
import pytz

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.conf import global_settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from transmeta import TransMeta

from avatar.models import Avatar
from avatar.templatetags import avatar_tags

from condottieri_profiles.defaults import *
from machiavelli.signals import government_overthrown, player_joined, player_surrendered


if "pinax.notifications" in settings.INSTALLED_APPS:
    from pinax.notifications import models as notification
else:
    notification = None

class CondottieriProfileManager(models.Manager):
    def hall_of_fame(self, order='weighted_score'):
        fields = [f.name for f in CondottieriProfile._meta.get_fields()]
        if not (order in fields \
            or order in ['avg_score', 'avg_victories']):
            order = 'weighted_score'
        order = ''.join(['-', order])
        return self.filter(total_score__gt=0, finished_games__gt=2).extra(
            select={'avg_victories': "100 * (victories / finished_games)",
                'avg_score': "total_score / finished_games"}).order_by(order)

class CondottieriProfile(models.Model):
    """ Defines the actual profile for a Condottieri user.

    """
    user = models.OneToOneField(User, verbose_name=_('user'), related_name='profile',
            on_delete=models.CASCADE)
    """ A User object related to the profile """
    name = models.CharField(_('name'), max_length=50, null=True, blank=True)
    """ The user complete name """
    about = models.TextField(_('about'), null=True, blank=True)
    """ More user info """
    location = models.CharField(_('location'), max_length=40, null=True, blank=True)
    """ Geographic location string """
    website = models.URLField(_("website"), null = True, blank = True)
    karma = models.PositiveIntegerField(default=KARMA_DEFAULT, editable=False)
    """ Total karma value """
    total_score = models.IntegerField(default=0, editable=False)
    """ Sum of game scores """
    weighted_score = models.IntegerField(default=0, editable=False)
    """ Sum of devaluated game scores """
    finished_games = models.PositiveIntegerField(default=0, editable=False)
    """ Number of games that the player has played to the end """
    victories = models.PositiveIntegerField(default=0, editable=False)
    """ Number of victories """
    overthrows = models.PositiveIntegerField(default=0, editable=False)
    """ Number of times that the player has been overthrown """
    surrenders = models.PositiveIntegerField(default=0, editable=False)
    """ Number of times that the player has surrendered """
    badges = models.ManyToManyField('Badge', verbose_name=_("badges"))
    is_editor = models.BooleanField(_("Is editor?"), default=False)
    """ Fields needed by pybbm """
    signature = models.TextField(_("Signature"), blank=True,
        max_length=SIGNATURE_MAX_LENGTH)
    signature_html = models.TextField(_("Signature HTML Version"), blank=True,
        max_length=SIGNATURE_MAX_LENGTH + 30)
    show_signatures = models.BooleanField(_("Show signatures"), blank=True,
        default=True)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)
    autosubscribe = models.BooleanField(_("Automatically subscribe"),
        help_text=_("Automatically subscribe to topics that you answer"),
        default=DEFAULT_AUTOSUBSCRIBE)

    objects = CondottieriProfileManager()

    def save(self, *args, **kwargs):
        if 'pybb' in settings.INSTALLED_APPS:
            from pybb.util import get_markup_engine
            markup = get_markup_engine()
            self.signature_html = markup.format(self.signature)   
        else:
            self.signature_html = self.signature
        super(CondottieriProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

    def has_languages(self):
        """ Returns true if the user has defined at least one known language """
        try:
            SpokenLanguage.objects.get(profile=self)
        except MultipleObjectsReturned:
            return True
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def average_score(self):
        if self.finished_games > 0:
            return float(self.total_score) / self.finished_games
        else:   
            return 0
    
    def adjust_karma(self, k):
        """ Adds or substracts some karma to the total """
        if not isinstance(k, int):
            return
        new_karma = self.karma + k
        if new_karma > KARMA_MAXIMUM:
            new_karma = KARMA_MAXIMUM
        elif new_karma < KARMA_MINIMUM:
            new_karma = KARMA_MINIMUM
        self.karma = new_karma
        self.save()

    def overthrow(self):
        """ Add 1 to the overthrows counter of the profile """
        self.overthrows += 1
        self.save()

    def check_karma_to_join(self, fast=False, private=False):
        if self.karma < KARMA_TO_JOIN:
            return _("You need a minimum karma of %s to play a game.") % \
                    KARMA_TO_JOIN
        if fast and self.karma < KARMA_TO_FAST:
            return _("You need a minimum karma of %s to play a fast game.") % \
                    KARMA_TO_FAST
        if private and self.karma < KARMA_TO_PRIVATE:
            return \
                _("You need a minimum karma of %s to create a private game.") \
                    % KARMA_TO_PRIVATE
        if self.karma < KARMA_TO_UNLIMITED:
            current_games = self.user.player_set.all().count()
            if current_games >= GAMES_LIMIT:
                return _("You need karma %s to play more than %s games.") % \
                        (KARMA_TO_UNLIMITED, GAMES_LIMIT)
        return ""

    ##
    ## Properties to proxy fields in PybbProfile
    ##
    def _get_time_zone(self):
        t = datetime.today()
        today = datetime(t.year, t.month, t.day)
        try:
            tz = pytz.timezone(self.user.account.timezone)
        except:
            return 0
        offset = float(tz.utcoffset(today).seconds) / 3600
        return offset
    
    time_zone = property(_get_time_zone)

    def _get_language(self):
        return self.user.account.language
    
    language = property(_get_language)

    def get_display_name(self):
        return self.user.username

def add_overthrow(sender, **kwargs):
    if not sender.voluntary:
        profile = sender.government.profile
        profile.overthrow()

government_overthrown.connect(add_overthrow)

def add_surrender(sender, **kwargs):
    profile = sender.user.profile
    profile.surrenders += 1
    try:
        surrender_karma = SURRENDER_KARMA
    except:
        surrender_karma = -10
    profile.adjust_karma(surrender_karma)

player_surrendered.connect(add_surrender)

def create_profile(sender, instance, created, raw, **kwargs):
    """ Creates a profile associated to a User  """
    if raw:
        return
    if instance is None:
        return
    ##The following line prevents pybb causing an IntegrityError when it tries
    ##to create the user profile for a second time.
    ##TODO: Look for a better solution.
    if 'pybb' in settings.INSTALLED_APPS:
        return
    profile, created = CondottieriProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)

class SpokenLanguage(models.Model):
    """ Defines a language that a User understands """
    code = models.CharField(_("language"), max_length=8, choices=global_settings.LANGUAGES)
    profile = models.ForeignKey(CondottieriProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_code_display()
    
    class Meta:
        unique_together = (('code', 'profile',),)

class Friendship(models.Model):
    """
    Defines a one-way friendship relationship between two users.
    """
    friend_from = models.ForeignKey(User, related_name="friends", on_delete=models.CASCADE)
    friend_to = models.ForeignKey(User, related_name="friend_of", on_delete=models.CASCADE)
    created_on = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        unique_together = (('friend_from', 'friend_to',),)

    def __str__(self):
        return "%s is a friend of %s" % (self.friend_to, self.friend_from)

def was_befriended(sender, instance, created, raw, **kwargs):
    """ Notify a user when other user befriends him """
    if notification and created and not raw:
        recipients = [instance.friend_to, ]
        extra_context = {'username': instance.friend_from,
                        'STATIC_URL': settings.STATIC_URL,}
        notification.send(recipients, "new_friend", extra_context)

post_save.connect(was_befriended, sender=Friendship)

def friend_joined_game(sender, **kwargs):
    """ Notify a user if a friend joins a game """
    if notification:
        user = sender.user
        friend_of_ids = user.friend_of.values_list('friend_from', flat=True)
        recipients = []
        for f in user.friends.all():
            if f.friend_to.id in friend_of_ids:
                recipients.append(f.friend_to)
        extra_context = {'username': sender.user.username,
                    'slug': sender.game.slug,
                    'STATIC_URL': settings.STATIC_URL,} 
        notification.send(recipients, "friend_joined", extra_context)

player_joined.connect(friend_joined_game)

class Badge(models.Model, metaclass=TransMeta):
    """ Defines an award or honor that a user may earn """

    image = models.ImageField(_("image"), upload_to="badges")
    description = models.CharField(_("description"), max_length=200)

    class Meta:
        verbose_name = _("badge")
        verbose_name_plural = _("badges")
        translate = ('description',)

    def __str__(self):
        return "%s" % self.description

