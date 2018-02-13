from django.forms import ModelForm

from condottieri_profiles.models import CondottieriProfile, SpokenLanguage

class ProfileForm(ModelForm):
    class Meta:
        model = CondottieriProfile
        exclude = ('user',
            'badges',
            'is_editor',
            'post_count',
            'signature',
            'signature_html',
            'show_signatures',)

class SpokenLanguageForm(ModelForm):
    class Meta:
        model = SpokenLanguage
        fields = ['code',]
