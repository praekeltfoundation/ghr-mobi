'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.core import constants as core_constants

from app.articles import models


class ArticleModelTestCase(TestCase):
    title = 'Article Model Title'
    slug = slugify(title)

    def setUp(self):
        '''
        Create an Article Model
        '''
        self.article_object = models.Article.objects.create(
            title=self.title,
        )

    def test_article_model(self):
        '''
        Test that the Article Model was created and has
        the correct state
        '''
        article_object = models.Article.objects.get(slug=self.slug)
        self.assertEqual(article_object.state, core_constants.STATE_PUBLISHED)
