# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import signals
from django.db.models.query import QuerySet

from dark_matter.commons import signals as commons_signals


class SoftDeleteQuerySet(QuerySet):

    def delete(self):
        self.update(is_active=False)
        for obj in self:
            signals.post_delete.send(sender=obj.__class__, instance=obj)

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()


class ActiveObjectsManager(models.Manager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True)

    def hard_delete(self):
        return getattr(self.get_queryset(), "hard_delete")()


class BaseModel(models.Model):
    """
    Abstract generic model used:
     1. to allow an object to be soft deleted instead removing it from db.
     2. Add Time information
    """
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveObjectsManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        """
        Method to soft delete an object
        """
        # TODO delete related objects
        signals.pre_delete.send(sender=self.__class__, instance=self)
        super(BaseModel, self).delete(**kwargs)
        self.is_active = False
        self.save()
        signals.post_delete.send(sender=self.__class__, instance=self)

    def restore(self):
        """
        Method to restore soft deleted object.
        If needed, add required signals
        """

        self.is_active = True
        self.save()

    def hard_delete(self, using=None):
        super(BaseModel, self).delete(using)


# Soft Delete other related objects in which referenced as Foreign Key or once-to-one field
# TODO: This does not work well with hard-delete. Investigate and fix
# signals.post_delete.connect(commons_signals.delete_related_objects)
