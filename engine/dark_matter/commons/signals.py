from django.contrib.auth import settings


def delete_related_objects(*args, **kwargs):
    """
    Soft delete all related object for soft deleted object
    """
    deleted_object = kwargs.get(u'instance')
    if deleted_object:
        for related_field in deleted_object._meta.get_all_related_objects():
            app_name = u'apps.{}'.format(related_field.related_model._meta.app_label)
            # Only delete related object of our own model. As we have added soft-delete logic in our models.
            if app_name in settings.LOCAL_APPS:
                related_object = getattr(deleted_object, related_field.get_accessor_name(), None)
                if related_field.one_to_many:  # Foreign key relation
                    related_object.all().delete()
                elif related_object:  # One-to-one relation
                    related_object.delete()
