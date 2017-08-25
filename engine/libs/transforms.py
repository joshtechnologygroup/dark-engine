from django.db import models


@models.TextField.register_lookup
@models.CharField.register_lookup
class InsensitiveSearch(models.Transform):
    """
    Django iexact does not support chained operations.
    Simple Transformer to overcome that limitation
    """
    lookup_name = u'iter_iexact'
    bilateral = True
    function = "UPPER"
