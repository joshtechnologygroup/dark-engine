# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator

from django.db.models import F
from django.db.models import Sum, Count
from nltk import (corpus)
from six import iteritems

from dark_matter.commons import parser as commons_parser
from dark_matter.keywords import models as keyword_models
from dark_matter.query_parser import models as query_models
from dark_matter.query_parser.models import QueryKeywordStore


class Parser(object):
    """
    Parses Search Query
    """

    FREQUENCY_FACTOR = 0.001
    PREV_SCORE_FACTOR = 0.1
    LEXICAL_SCORE_FACTOR = 0.8

    def __init__(self, query):
        self.query = query
        self.query_object = None
        self.initialize()

    def initialize(self):
        """
        Perform Initial actions with query
        """
        self.save_query()

    def save_query(self):
        self.query_object = query_models.QueryStore.objects.create(text=self.query)

    def keyword_processor(self):
        keywords_with_weights = self.extract_keywords()
        self.save_keywords(keywords_with_weights)

    def extract_keywords(self):
        """
        Extract Keywords from Query
        :return
        [
            (keyword1, Normalized_score_1),
            (keyword2, Normalized_score_2),
        ]
        """

        stopwords = corpus.stopwords.words('english')
        rake = commons_parser.IndexingDrake(stopwords)
        keywords_with_weight = rake.run(self.query)
        enhanced_keywords_with_weight = self.process_past_queries(keywords_with_weight)
        return sorted(enhanced_keywords_with_weight.items(), key=operator.itemgetter(1), reverse=True)

    def process_past_queries(self, keywords_with_weight):
        past_queries = QueryKeywordStore.objects.filter(
            keyword__keyword__in=[keyword[0] for keyword in keywords_with_weight]
        ).annotate(phrase=F('keyword__keyword')).values('phrase').annotate(
            frequency=Count('keyword'), sum=Sum('score')).values_list('phrase', 'sum', 'frequency')

        # convert list of tuples to dict to allow assignment
        keywords_with_weight_dict = {}
        for keyword in keywords_with_weight:
            keywords_with_weight_dict[keyword[0]] = keyword[1]

        # convert list of tuples to dict
        past_queries_dict = {}
        for row in past_queries:
            past_queries_dict.update({row[0]: [row[1], row[2]]})

        # update current score, prev score calculated as average_weight*frequency
        for keyword, score in iteritems(keywords_with_weight_dict):
            if past_queries_dict.get(keyword):
                prev_score_average = past_queries_dict[keyword][0] / past_queries_dict[keyword][1]
                score = self.LEXICAL_SCORE_FACTOR * score + \
                        self.PREV_SCORE_FACTOR * prev_score_average + \
                        self.FREQUENCY_FACTOR * past_queries_dict[keyword][1]
                keywords_with_weight_dict[keyword] = score
            else:
                keywords_with_weight_dict[keyword] = .8 * score

        return keywords_with_weight_dict

    def save_keywords(self, weighted_keywords):

        obj_list = []

        for kw, weight in weighted_keywords:
            keyword, _ = keyword_models.Keywords.objects.get_or_create(keyword=kw)
            obj_list.append(query_models.QueryKeywordStore(query=self.query_object, keyword=keyword, score=weight))

        query_models.QueryKeywordStore.objects.bulk_create(obj_list)
