'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.poll import models as poll_models
from tunobase.core import constants as core_constants

from app.research_tool import models


class ResearchToolModelTestCase(TestCase):
    title = 'Research Tool Model Title'
    question = 'Test Poll Question'
    slug = slugify(title)

    def setUp(self):
        '''
        Create a Research Tool Model
        '''
        self.poll = poll_models.PollQuestion.objects.create(
            question=self.question)

        self.research_tool_object = models.ResearchTool.objects.create(
            title=self.title,
            poll=self.poll
        )

    def test_research_tool_model(self):
        '''
        Test that the Research Tool Model was created, has a poll
        and is in the correct state
        '''
        research_tool_object = models.ResearchTool.objects.get(slug=self.slug)
        self.assertEqual(research_tool_object.state,
                         core_constants.STATE_PUBLISHED)
        self.assertEqual(research_tool_object.poll, self.poll)
