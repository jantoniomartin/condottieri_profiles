## django
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

## condottieri_profiles
import condottieri_profiles.models as profiles
import condottieri_profiles.forms as forms

@login_required
def profile_detail(request, username=''):
	user = get_object_or_404(User, username=username)
	profile = user.get_profile()
	is_own = (request.user == user)
	friends = user.friends.all()
	chosen_by = user.friend_of.all()
	is_friend = am_friend = False
	if not is_own:
		is_friend = user.id in request.user.friends.values_list('friend_to', flat=True)
		am_friend = request.user.id in user.friend_of.values_list('friend_to', flat=True)
	context = {
		'profile': profile,
		'friends': friends,
		'chosen_by': chosen_by,
		'is_own' : is_own,
		'is_friend': is_friend,
		'am_friend': am_friend,
	}

	return render_to_response('condottieri_profiles/profile_detail.html',
							context,
							context_instance=RequestContext(request))

@login_required
def profile_edit(request):
	profile = request.user.get_profile()
	if request.method == 'POST':
		form = forms.ProfileForm(data=request.POST, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, _("Your profile has been updated."))
			return redirect(profile)
	else:	
		form = forms.ProfileForm(instance=profile)

	return render_to_response('condottieri_profiles/profile_form.html',
							{'form': form,},
							context_instance=RequestContext(request))

@login_required
def languages_edit(request):
	profile = request.user.get_profile()
	LangInlineFormSet = inlineformset_factory(profiles.CondottieriProfile, profiles.SpokenLanguage, extra=1)
	if request.method == 'POST':
		formset = LangInlineFormSet(request.POST, instance=profile)
		if formset.is_valid():
			formset.save()
			messages.success(request, _("Your languages have been updated."))
			return redirect(profile)
	else:
		formset = LangInlineFormSet(instance=profile)

	return render_to_response('condottieri_profiles/language_form.html',
							{'formset': formset,},
							context_instance=RequestContext(request))

@login_required
def change_friendship(request, username=''):
	user_from = request.user
	user_to = get_object_or_404(User, username=username)
	try:
		friendship = profiles.Friendship.objects.get(friend_from=user_from, friend_to=user_to)
	except ObjectDoesNotExist:
		friendship = profiles.Friendship.objects.create(friend_from=user_from, friend_to=user_to)
		friendship.save()
		msg = _("%s is now your friend.") % user_to.username
	else:
		friendship.delete()
		msg = _("%s is no longer your friend.") % user_to.username
	messages.success(request, msg)
	return redirect(user_to.get_profile())

	
