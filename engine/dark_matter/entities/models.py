# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager

from dark_matter.commons import models as commons_models


class Document(commons_models.BaseModel):
    """
    Stores document information
    """

    file = models.FileField()
    is_parsed = models.BooleanField(default=False)

    tags = TaggableManager()

    def __unicode__(self):
        return self.file.name


class Entity(commons_models.BaseModel):
    """
    Stores Entity Information
    """

    entity = models.TextField()
    document = models.ForeignKey(Document)

    class Meta:
        verbose_name_plural = 'Entities'

    def __unicode__(self):
        return self.entity
