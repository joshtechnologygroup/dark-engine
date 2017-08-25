# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# TODO: This is rough View

from dark_matter.query_parser import parser as query_parser
from dark_matter.search_engine import ranker


def search_query(query_string):
    qp = query_parser.Parser(query_string)
    qp.keyword_processor()
    return ranker.Ranker(qp.query_object.id).processor()
