from django.conf.urls.defaults import *
#from django.views.generic import list_detail
#from django.views.generic.create_update import create_object
from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page

from condottieri_profiles.views import *

urlpatterns = patterns('condottieri_profiles.views',
	url(r'^profile/(?P<slug>\w+)$',
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

