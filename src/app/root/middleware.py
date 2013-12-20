'''
Created on 08 Nov 2013

@author: michael
'''
import re

from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.utils import timezone, dateparse
from django.contrib.contenttypes.models import ContentType

from app.root import models
from app.articles import models as ArticleModel


class UserTrackingMiddleware(object):
    '''
    Enable this Middleware to track Users
    on the site
    '''

    def process_response(self, request, response):
        site_visited = request.COOKIES.get('site_visited', False)

        if site_visited:
            site_visited = dateparse.parse_datetime(site_visited)
            now = timezone.now()

            if not site_visited.day == now.day and not \
               site_visited.month == now.month:
                models.Visitor.objects.create()
                response.set_cookie(
                    'site_visited',
                    timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    60 * 60 * 24 * 30
                )
        else:
            models.Visitor.objects.create(unique=True)
            response.set_cookie(
                'site_visited',
                timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                60 * 60 * 24 * 30
            )

        return response


class PageImpressionMiddleware(object):
    '''
    Enable this Middleware to make the entire
    site Age-Gated
    '''

    def process_template_response(self, request, response):
        extra_kwargs = {}
        if request.resolver_match.url_name == 'article_detail':
            obj = response.context_data['object']
            extra_kwargs.update({
                'content_type_id': ContentType.objects.get_for_model(obj).id,
                'object_pk': obj.pk
            })

        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        models.PageImpression.objects.create(
            user=user,
            path=request.path_info,
            user_agent=request.META['HTTP_USER_AGENT'],
            **extra_kwargs
        )

        return response
