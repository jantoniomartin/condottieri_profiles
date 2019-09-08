# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'badges', verbose_name='image')),
                ('description_en', models.CharField(max_length=200, null=True, verbose_name='description', blank=True)),
                ('description_es', models.CharField(max_length=200, null=True, verbose_name='description', blank=True)),
                ('description_ca', models.CharField(max_length=200, null=True, verbose_name='description', blank=True)),
                ('description_de', models.CharField(max_length=200, null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'badge',
                'verbose_name_plural': 'badges',
            },
        ),
        migrations.CreateModel(
            name='CondottieriProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, verbose_name='name', blank=True)),
                ('about', models.TextField(null=True, verbose_name='about', blank=True)),
                ('location', models.CharField(max_length=40, null=True, verbose_name='location', blank=True)),
                ('website', models.URLField(null=True, verbose_name='website', blank=True)),
                ('karma', models.PositiveIntegerField(default=100, editable=False)),
                ('total_score', models.IntegerField(default=0, editable=False)),
                ('weighted_score', models.IntegerField(default=0, editable=False)),
                ('finished_games', models.PositiveIntegerField(default=0, editable=False)),
                ('victories', models.PositiveIntegerField(default=0, editable=False)),
                ('overthrows', models.PositiveIntegerField(default=0, editable=False)),
                ('surrenders', models.PositiveIntegerField(default=0, editable=False)),
                ('is_editor', models.BooleanField(default=False, verbose_name='Is editor?')),
                ('signature', models.TextField(max_length=1024, verbose_name='Signature', blank=True)),
                ('signature_html', models.TextField(max_length=1054, verbose_name='Signature HTML Version', blank=True)),
                ('show_signatures', models.BooleanField(default=True, verbose_name='Show signatures')),
                ('post_count', models.IntegerField(default=0, verbose_name='Post count', blank=True)),
                ('autosubscribe', models.BooleanField(default=True, help_text='Automatically subscribe to topics that you answer', verbose_name='Automatically subscribe')),
                ('badges', models.ManyToManyField(to='condottieri_profiles.Badge', verbose_name='badges')),
                ('user', models.OneToOneField(related_name='profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('friend_from', models.ForeignKey(related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('friend_to', models.ForeignKey(related_name='friend_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpokenLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=8, verbose_name='language', choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('profile', models.ForeignKey(to='condottieri_profiles.CondottieriProfile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='spokenlanguage',
            unique_together=set([('code', 'profile')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('friend_from', 'friend_to')]),
        ),
    ]
