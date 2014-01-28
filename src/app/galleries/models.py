from django.core.urlresolvers import reverse

from tunobase.core import models

def get_absolute_url(self):
    return reverse('gallery_detail', args=[self.slug,])

models.Gallery.get_absolute_url = get_absolute_url