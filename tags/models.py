from django.db import models
""" WE DONT WANT THIS TO HAPPEN => Sol: use generic relationships
# tags app is dependant on store app
from store.models import Product
"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)
class TaggedItem(models.Model):
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # We need 3 things to use generic relationships
    # =============================================
    # -Type (product, video, article)
    # -ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)# <= use abstract model instead of (Product)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()