# Copyright (c) 2009 James Aylett <http://tartarus.org/james/computers/django/>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django.template.defaultfilters import slugify
from django.db import models

def suggest_slug(objects, name):
    """Given a QuerySet and the name of a new object, figure out an acceptable unused slug."""
    if not name:
        return ''
    slug = slugify(name)
    original_slug = slug
    suffix = None
    while objects.filter(slug = slug).count():
        if suffix is None:
            suffix = 1
        else:
            suffix += 1
        slug = original_slug + '-' + str(suffix)
    return slug

class SluggableModel(models.Model):
    "Automatically generate the slug field as necessary from the name field. By default will be made unique within the model."
    slug = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    @classmethod
    def slug_objects(cls):
        "Default to checking across all objects for conflicting slugs. Override this if slugs only have to be unique across a subset."
        return cls.objects
    
    def generate_slug(self, force=False):
        "Auto-generate the slug as needed."
        if not self.slug:
            self.slug = suggest_slug(type(self).slug_objects(), self.name)

    def save(self, *args, **kwargs):
        "On save, generate slug if needed."
        self.generate_slug()
        super(SluggableModel, self).save(*args, **kwargs)
