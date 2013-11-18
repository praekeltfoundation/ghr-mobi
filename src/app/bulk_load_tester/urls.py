from django.conf.urls import patterns, include, url

from tunobase.bulk_loading.views import BulkUpload

from app.bulk_load_tester import forms, bulk_updaters

urlpatterns = patterns('',
    url(r'^bulk-load-articles/$',
        BulkUpload.as_view(
            validator_form_class=forms.ArticleBulkUploadValidatorForm,
            unique_field_names=['title', 'plain_content'],
            bulk_updater_class=bulk_updaters.BulkUpdaterTest
        ),
        name='bulk_load_articles'
    ),
)