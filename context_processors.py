from django.core.cache import cache

from condottieri_profiles.models import CondottieriProfile
from condottieri_common.models import Server

def sidebar_ranking(request):
	if request.user.is_authenticated:
		user_id = request.user.id
	else:
		user_id = None
	cache_key = "sidebar_ranking-%s" % user_id
	context = cache.get(cache_key)
	if not context:
		context = {}
		top_users = CondottieriProfile.objects.all().order_by('-weighted_score')[:5]
		if not user_id is None:
			profile = request.user.profile
			if not profile in top_users:
				my_score = profile.weighted_score
				my_position = CondottieriProfile.objects.filter(weighted_score__gt=my_score).count() + 1
				context.update({'my_position': my_position,})
		server = Server.objects.get()
		context['ranking_last_update'] = server.ranking_last_update
		context['top_users'] = top_users
		cache.set(cache_key, context)
	return context
