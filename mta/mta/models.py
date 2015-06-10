from django.db import models
from django.contrib.auth.models import User


class FavoriteLine(models.Model):
    user = models.ForeignKey(User)
    service = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    status = models.TextField(blank=True, null='')

    def __unicode__(self):
        return "%s" % str( self.name )
