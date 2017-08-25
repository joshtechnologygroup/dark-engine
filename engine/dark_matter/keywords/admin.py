# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from dark_matter.keywords import models as keyword_models


class KeywordAdmin(admin.ModelAdmin):
    """
    Entity Admin
    """


admin.site.register(keyword_models.Keywords, KeywordAdmin)
