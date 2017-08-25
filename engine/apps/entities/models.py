# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from engine.apps.commons import models as commons_models
# from apps.commons import models as commons_models


class Document(commons_models.BaseModel):
    """
    Stores document information
    """

    file = models.FileField()


class Entity(commons_models.BaseModel):
    """
    Stores Entity Information
    """

    entity = models.TextField()
    document = models.ForeignKey(Document)
