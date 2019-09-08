from django.conf.urls import url

from condottieri_profiles.views import *

urlpatterns = [
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
]
