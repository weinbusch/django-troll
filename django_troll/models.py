from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

class Comment(models.Model):
    
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_pk')
    
    comment = models.TextField(_('comment'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now=True)