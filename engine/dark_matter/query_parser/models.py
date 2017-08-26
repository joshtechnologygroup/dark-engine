# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

from dark_matter.commons import models as commons_models
from dark_matter.keywords import models as keywords_models


class QueryStore(commons_models.BaseModel):
    """
    Stores all Queries
    """

    text = models.TextField()

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'

    def __unicode__(self):
        return self.text


class QueryKeywordStore(commons_models.BaseModel):
    """
    Stores Relationship between query and keywords
    """

    query = models.ForeignKey(QueryStore)
    keyword = models.ForeignKey(keywords_models.Keywords)
    score = models.FloatField()
    score_doc = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Query Keyword Score'
        verbose_name_plural = 'Query Keyword Scores'

    def __unicode__(self):
        return "{} - {}".format(self.query.text, self.keyword.keyword)
