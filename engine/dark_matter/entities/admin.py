# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from dark_matter.entities import models as entity_models


class EntityAdmin(admin.ModelAdmin):
    """
    Entity Admin
    """


class DocumentAdmin(admin.ModelAdmin):
    """
    Document Admin
    """


admin.site.register(entity_models.Entity, EntityAdmin)
admin.site.register(entity_models.Document, DocumentAdmin)
