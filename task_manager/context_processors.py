from django.conf import settings
from django.utils import translation

def language_context(request):
    return {
        'LANGUAGES': settings.LANGUAGES,
        'LANGUAGE_CODE': translation.get_language(),
    }