=====================
django_auto_sluggable
=====================

Very simple Django extension that provides an auto-generated slug field to a Django model.

Use it something like:

----------------------------------------------------------------------------
from django.db import models
from django_auto_sluggable.models import SluggableModel

class MyModel(SluggableModel):
    name = models.CharField(max_length=255)
		
    def __unicode__(self):
        return self.name
----------------------------------------------------------------------------

The abstract model SluggableModel includes a slug field, and manages it for you. Note that the slug field is *not* marked as unique=True in the Django field definition, and hence will not have an index generated by default; you probably want to add one yourself.

When you create a new MyModel, its slug will be generated from the name field, unique across all instances.

If you instead want the slug to be unique across a subset of all your objects (say because your URLs look like /users/<username>/articles/<slug> and so the article slug only needs to be unique within a user) do something like:

----------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django_auto_sluggable.models import SluggableModel

class Article(SluggableModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
		
    def slug_objects(self):
        return type(self).objects.filter(user=self.user)

    def __unicode__(self):
        return u"%s: %s" % (self.user, self.name,)
----------------------------------------------------------------------------

Finally, if you don't have a name field, you can do something like:

----------------------------------------------------------------------------
from django.db import models
from django_auto_sluggable.models import SluggableModel

class Paper(SluggableModel):
    title = models.CharField(max_length=255)
		
    @property
    def name(self):
        return self.title
		
    def __unicode__(self):
        return self.title
----------------------------------------------------------------------------

Alternatively, you could change SluggableModel itself to make the field used to generate the slug configurable; that's left as an exercise for the reader ;-)

James Aylett <http://tartarus.org/james/computers/django/>