from django.test import TestCase
from django.template.defaultfilters import slugify
from tunobase.core import utils as core_utils,constants as core_constants, models as core_models

class GalleryModelTestCase(TestCase):
    title = 'Gallery Model Title'
    slug = slugify(title)

    def setUp(self):
        '''
        Create an Gallery Model
        '''
        self.gallery_object = core_models.Gallery.objects.create(
            title=self.title,
        )

    def test_gallery_model(self):
        '''
        Test that the Gallery Model was created and has
        the correct state
        '''
        gallery_object = core_models.Gallery.objects.get(slug=self.slug)
        self.assertEqual(gallery_object.state, core_constants.STATE_PUBLISHED)