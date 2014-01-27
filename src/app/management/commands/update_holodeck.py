'''
Created on 23 Jan 2014

@author: michael
'''
from django.core.management.base import BaseCommand

from app.root import metrics


class Command(BaseCommand):
    """
    Update holodeck metrics
    """

    def handle(self, *args, **options):
        metrics.push_total_users()
        metrics.push_unique_users()
        metrics.push_page_views()
        metrics.push_newsfeed_page_views()
        metrics.push_registrations()
        metrics.push_comments()
        metrics.push_likes()
        metrics.push_research_tool_polls()
        metrics.push_top_5_articles_page_views()
        metrics.push_top_5_articles_comments()
