## django
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView
from django.views.generic.base import RedirectView

from extra_views import InlineFormSet, UpdateWithInlinesView

## condottieri_profiles
from condottieri_profiles.models import *
from condottieri_profiles.forms import *

class LoginRequiredMixin(object):
	##TODO: move this to middleware
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ProfileDetailView(LoginRequiredMixin, DetailView):
	model = User
	template_name = 'condottieri_profiles/profile_detail.html'
	slug_field = 'username'
	slug_url_kwarg = 'username'

	def get_context_data(self, **kwargs):
		ctx = super(ProfileDetailView, self).get_context_data(**kwargs)
		is_friend = am_friend = None
		ctx.update({
			'profile': self.object.get_profile(),
			'friends': self.object.friends.all(),
			'chosen_by': self.object.friend_of.all(),
			'is_own': self.request.user == self.object,
		})
		if self.request.user != self.object:
			ctx.update({
				'is_friend': self.object.id in self.request.user.friends. \
						values_list('friend_to', flat=True),
				'am_friend': self.request.user.id in self.object.friend_of. \
						values_list('friend_to', flat=True),
			})
		return ctx

class LanguagesInline(InlineFormSet):
	model = SpokenLanguage
	extra = 1

class ProfileUpdateView(LoginRequiredMixin, UpdateWithInlinesView):
	model = CondottieriProfile
	form_class = ProfileForm
	template_name = 'condottieri_profiles/profile_form.html'
	inlines = [LanguagesInline,]

	def get_object(self, queryset=None):
		return self.request.user.get_profile()

	def get_success_url(self):
		messages.success(self.request, _("Your profile has been updated."))
		return self.request.user.get_profile().get_absolute_url()

class ToggleFriendshipView(LoginRequiredMixin, RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		user_from = self.request.user
		user_to = get_object_or_404(User, username=self.kwargs['username'])
		try:
			friendship = Friendship.objects.get(
				friend_from=user_from,
				friend_to=user_to
			)
		except ObjectDoesNotExist:
			friendship = Friendship.objects.create(
				friend_from=user_from,
				friend_to=user_to
			)
			friendship.save()
			msg = _("%s is now your friend.") % user_to.username
		else:
			friendship.delete()
			msg = _("%s is no longer your friend.") % user_to.username
		messages.success(self.request, msg)
		return user_to.get_profile().get_absolute_url()

