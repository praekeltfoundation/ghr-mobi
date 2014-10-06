"""
    This module is used for display the 
    image numbers with total image numbers
"""
from django import template
register = template.Library()


@register.assignment_tag
def getCountValue(gallery, gallery_image):
    gallery_images = tuple(gallery.images.order_by("id"))
    return {
        'current_image': gallery_images.index(gallery_image)+1,
        'total_count': len(gallery_images)
    }
