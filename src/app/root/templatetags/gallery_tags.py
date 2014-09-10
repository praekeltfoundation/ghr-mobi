"""
    This module is used for display the image numbers with total image numbers
"""
from django import template
register = template.Library()


@register.assignment_tag
def getCountValue(gallery, gallery_image_pk):
    gallery_images = list(gallery.images.all().reverse())
    return {
        'current_image': gallery_images.index(gallery_image_pk)+1,
        'total_count': len(gallery_images)
    }
