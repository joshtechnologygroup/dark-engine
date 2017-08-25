# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from dark_matter.search_engine import models as search_models


class EntityScoreAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'entity', 'score')
    raw_id_fields = ('keyword', 'entity')


admin.site.register(search_models.EntityScore, EntityScoreAdmin)
