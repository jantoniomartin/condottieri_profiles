from django.conf.urls import *

from condottieri_profiles.views import *

urlpatterns = patterns('condottieri_profiles.views',
	url(r'^profile/(?P<username>\w+)$',
		ProfileDetailView.as_view(),
		name='profile_detail'
	),
	url(r'^edit$',
		ProfileUpdateView.as_view(),
		name='profile_edit'
	),
	url(r'^profile/f/(?P<username>\w+)$',
		ToggleFriendshipView.as_view(),
		name='change_friendship'
	),
)

