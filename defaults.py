from django.conf import settings

KARMA_MINIMUM = getattr(settings, 'KARMA_MINIMUM', 10)

KARMA_DEFAULT = getattr(settings, 'KARMA_DEFAULT', 100)

KARMA_MAXIMUM = getattr(settings, 'KARMA_MAXIMUM', 200)

KARMA_TO_JOIN = getattr(settings, 'KARMA_TO_JOIN', 70)

KARMA_TO_FAST = getattr(settings, 'KARMA_TO_FAST', 110)

KARMA_TO_PRIVATE = getattr(settings, 'KARMA_TO_PRIVATE', 110)

KARMA_TO_UNLIMITED = getattr(settings, 'KARMA_TO_UNLIMITED', 130)

KARMA_TO_REVOLUTION = getattr(settings, 'KARMA_TO_REVOLUTION', 170)

SURRENDER_KARMA = getattr(settings, 'SURRENDER_KARMA', -10)

GAMES_LIMIT = getattr(settings, 'GAMES_LIMIT', 50)


if 'pybb' in settings.INSTALLED_APPS:
	import pybb.defaults

	SIGNATURE_MAX_LENGTH = pybb.defaults.PYBB_SIGNATURE_MAX_LENGTH
	DEFAULT_AUTOSUBSCRIBE = pybb.defaults.PYBB_DEFAULT_AUTOSUBSCRIBE
	MARKUP_ENGINE = pybb.defaults.PYBB_MARKUP_ENGINES[pybb.defaults.PYBB_MARKUP]
else:
	SIGNATURE_MAX_LENGTH = 1024
	DEFAULT_AUTOSUBSCRIBE = True
	MARKUP_ENGINE = None
