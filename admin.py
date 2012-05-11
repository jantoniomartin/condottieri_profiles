import condottieri_profiles.models as profiles
from django.contrib import admin

class SpokenLanguageInline(admin.TabularInline):
	model = profiles.SpokenLanguage
	extra = 1

class CondottieriProfileAdmin(admin.ModelAdmin):
	ordering = ['user__username']
	list_display = ('__unicode__', 'location', 'website', 'karma', 'total_score', 'weighted_score', 'overthrows')
	inlines = [SpokenLanguageInline,]

admin.site.register(profiles.CondottieriProfile, CondottieriProfileAdmin)
admin.site.register(profiles.Friendship)
admin.site.register(profiles.Badge)
