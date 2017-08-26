# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from dark_matter.query_parser import models as query_models


class QueryAdmin(admin.ModelAdmin):
    """
    Query Admin
    """


class QueryKeywordStoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'query', 'keyword', 'score')


admin.site.register(query_models.QueryStore, QueryAdmin)
admin.site.register(query_models.QueryKeywordStore, QueryKeywordStoreAdmin)
