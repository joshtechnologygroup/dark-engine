import RAKE
from nltk import (corpus, WordNetLemmatizer, Counter)

from engine.dark_matter.query_parser.models import QueryStore, QueryKeywordStore


class Parser(object):
    """
    Parses Search Query
    """

    def __init__(self, query):
        self.query = query

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

        query_terms = self.query.split(' ')
        lemmatized_query = [WordNetLemmatizer().lemmatize(query_term) for query_term in query_terms]
        keywords_with_weight = rake.run(' '.join(lemmatized_query))

        max_weight = 0
        for x in keywords_with_weight:
            if x[1] > max_weight:
                max_weight = x[1]

        normalized_keywords_with_weight = []

        if not max_weight:
            # No Data extracted
            return [[]]

        for x in keywords_with_weight:
            normalized_keywords_with_weight.append([x[0], x[1] / max_weight])

        for keyword in normalized_keywords_with_weight:
            query_store = QueryStore(self.query)
            query_store.save()
            QueryKeywordStore(query=query_store, keyword=keyword[0], score=keyword[1]).save()
        return normalized_keywords_with_weight

    def process_past_queries(self, keywords_with_weight):
        past_keywords_store = QueryKeywordStore.objects.filter(keyword__in=[keyword[0] for keyword in
                                                                            keywords_with_weight])
        score = {}
        past_keywords_count = Counter(keyword.keyword for keyword in past_keywords_store)
        for keyword in past_keywords_store:
            if not score.get(keyword):
                score[keyword] = keyword.score
                past_keywords_store[keyword] = 1
            else:
                score[keyword] += keyword.score
                past_keywords_store[keyword] += 1

        for keyword in keywords_with_weight:
            score[keyword] /= past_keywords_count.get(keyword)

        for keyword in keywords_with_weight:
            keyword[1] += score[keyword]

        max_weight = 0
        for x in keywords_with_weight:
            if x[1] > max_weight:
                max_weight = x[1]

        normalized_keywords_with_weight = []

        if not max_weight:
            # No Data extracted
            return [[]]

        for x in keywords_with_weight:
            normalized_keywords_with_weight.append([x[0], x[1] / max_weight])

        return normalized_keywords_with_weight
