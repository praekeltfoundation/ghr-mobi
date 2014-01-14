from django.conf import settings
from django.contrib.sites.models import Site


def project_settings(request):
    return {'DEBUG': settings.DEBUG,
            'site': Site.objects.get_current()}
