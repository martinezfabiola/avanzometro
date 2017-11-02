from django.apps import AppConfig
from django.utils import translation


class GraficoConfig(AppConfig):
    name = 'grafico'

class LocaleMiddleware(object):

    def process_request(self, request):
        language = translation.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()