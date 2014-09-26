from django.test import TestCase
from tunobase.core import utils as core_utils, constants\
    as core_constants, models as core_models
from django.template.defaultfilters import slugify
from django.template import Template, Context


class GalleryModelTestCase(TestCase):
    title = 'Gallery Model Title'
    image_name = 'MyImage'
    slug = slugify(title)

    def setUp(self):
        '''
        Create an Gallery Model
        '''
        self.gallery_object = core_models.Gallery.objects.create(
            title=self.title,
        )
        for image_no in range(4):
            
            self.gallery_image_object = self.gallery_object.images.create(
                image_name='%s %i' % (self.image_name, image_no),
            )
            
    def test_gallery_model(self):
        '''
        Test that the Gallery Model was created and has
        the correct state
        '''
        gallery_object = core_models.Gallery.objects.get(slug=self.slug)
        self.assertEqual(gallery_object.state, core_constants.STATE_PUBLISHED)

    def test_get_count_value(self):
        gallery_object = core_models.Gallery.objects.get(slug=self.slug)
        gallery_image_object = gallery_object.images.all()[1]
        t = Template('{% load gallery_tags %}{% getCountValue gallery_object gallery_image_object as count_value %}')
        c = Context({"gallery_object": self.gallery_object, "gallery_image_object": self.gallery_image_object})
        t.render(c)
        self.assertEqual(c['count_value'], {'current_image': 2, 'total_count': 4})