'''
Created on 20 Nov 2013

@author: michael
'''
from collections import namedtuple

from django.test import TestCase
from django.contrib.auth.models import Group

from app.root.templatetags import root_widgets
from app.authentication import models as auth_models
from app.discussions import models as discussion_models


class HomePageDiscussionWidgetTestCase(TestCase):

    def setUp(self):
        '''
        Create authenticated user and unauthenticated user
        '''
        journalists_group = Group.objects.create(
            name='Ni Nyampinga Journalists'
        )
        ambassadors_group = Group.objects.create(
            name='Ambassadors'
        )

        self.discussion = discussion_models.Discussion.objects.create(
            title='Test Discussion',
            for_ni_nyampinga_journalists_only=True
        )

        self.authenticated_user_object = auth_models.EndUser.objects\
            .create_user(
            username='autheduser',
            password='1234'
        )
        self.authenticated_user_object.save()
        self.authenticated_user_object.groups.add(
            journalists_group,
            ambassadors_group
        )

        self.unauthenticated_user_object = auth_models.EndUser.objects\
            .create_user(
            username='unautheduser',
            password='1234'
        )

    def test_homepage_discussion_widget(self):
        '''
        Test that the HomePage discussion widget
        works as intended
        '''
        Request = namedtuple('Request', ['user'])

        request = Request((self.authenticated_user_object))
        authed_context = root_widgets.home_page_discussion_widget({
            'request': request
        })
        self.assertEqual(len(authed_context['object_list']), 1)

        request = Request((self.unauthenticated_user_object))
        unauthed_context = root_widgets.home_page_discussion_widget({
            'request': request
        })
        self.assertEqual(len(unauthed_context['object_list']), 0)
