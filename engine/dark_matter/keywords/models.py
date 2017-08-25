# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from dark_matter.commons import models as commons_models


class Keywords(commons_models.BaseModel):
    """
    Stores keywords information
    """

    keyword = models.TextField()
