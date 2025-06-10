from django.utils import translation

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get('lang', 'uz')
        translation.activate(lang if lang in ['uz', 'en'] else 'uz')
        response = self.get_response(request)
        translation.deactivate()
        return response