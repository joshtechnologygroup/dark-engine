# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

from dark_matter.commons import models as commons_models
from dark_matter.entities import models as entities_models
from dark_matter.keywords import models as keywords_models


class EntityScore(commons_models.BaseModel):
    """
    Stores Relationship between entity and keywords
    """

    entity = models.ForeignKey(entities_models.Entity)
    keyword = models.ForeignKey(keywords_models.Keywords)
    score = models.FloatField()
    score_document = JSONField("Document to store information related to scoring", null=True, blank=True)

    def __unicode__(self):
        return "{} - {}".format(self.keyword, self.entity)


class DocumentStore(commons_models.BaseModel):
    """
    Stores Relationship between doucments and keywords
    """

    document = models.ForeignKey(entities_models.Entity)
    keyword = models.ForeignKey(keywords_models.Keywords)
    score = models.IntegerField()
    score_document = JSONField("Document to store information related to scoring")
