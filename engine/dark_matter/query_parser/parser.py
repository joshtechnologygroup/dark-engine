import RAKE
from nltk import corpus

from dark_matter.query_parser import models as query_models
from dark_matter.keywords import models as keyword_models


class Parser(object):
    """
    Parses Search Query
    """

    def __init__(self, query):
        self.query = query
        self.query_id = None
        self.initialize()

    def initialize(self):
        """
        Perform Initial actions with query
        """
        self.save_query()

    def save_query(self):
        self.query_id = query_models.QueryStore.objects.create(text=self.query)

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
        rake = RAKE.Rake(stopwords)

        max_weight = 0
        keywords_with_weight = rake.run(self.query)

        for x in keywords_with_weight:
            if x[1] > max_weight:
                max_weight = x[1]

        normalized_keywords_with_weight = []

        if not max_weight:
            # No Data extracted
            return [[]]

        for x in keywords_with_weight:
            normalized_keywords_with_weight.append((x[0], x[1] / max_weight))

        return normalized_keywords_with_weight

    def save_keywords(self, weighted_keywords):

        obj_list = []

        for kw, weight in weighted_keywords:
            keyword, _ = keyword_models.Keywords.objects.get_or_create(keyword=kw)
            obj_list.append(query_models.QueryKeywordStore(query=self.query_id, keyword=keyword, score=weight))

        query_models.QueryKeywordStore.objects.bulk_create(obj_list)
