from operator import itemgetter

from django.db import connection

from dark_matter.search_engine import (
    constants as search_constants,
)
from dark_matter.search_engine.similarity_checker import similarity


class Ranker(object):

    def __init__(self, query_object):
        """
        Expected that query_object will be of Type QueryStore representing current query fired
        """

        self.query_object = query_object

    def processor(self):
        """
        Basic processor which only needs List of Keywords to operate on
        """

        # TODO: Should exclude soft-deleted object

        query = """
        SELECT
          tbl_entity.entity AS entity_text,
          sq.entity_score
        FROM (
               SELECT
                 tbl_entity_score.entity_id,
                 -- (sum(tbl_entity_score.score * tbl_query_word_store.score * tbl_keyword_match.f1_score) / --optimization
                 (sum(tbl_query_word_store.score * tbl_keyword_match.f1_score) /
                  avg(tbl_query_word_store.sum_all_scores)) AS entity_score
               FROM
                 (SELECT
                    tbl_keywords.keyword_id,
                    tbl_query_keywords.keyword_id                              AS query_keyword_id,
                    2 * (count(tbl_keywords.key) / avg(tbl_query_keywords.total_keys)) *
                    (count(tbl_keywords.key) / avg(tbl_keywords.total_keys)) /
                    ((count(tbl_keywords.key) / avg(tbl_query_keywords.total_keys)) +
                     (count(tbl_keywords.key) / avg(tbl_keywords.total_keys))) AS f1_score
                  FROM
                    (
                      SELECT
                        id                                                                AS keyword_id,
                        char_length(keyword) - char_length(replace(keyword, ' ', '')) + 1 AS total_keys,
                        regexp_split_to_table(keyword, ' ')                               AS key
                      FROM public.keywords_keywords
                      WHERE id IN (SELECT keyword_id
                                   FROM public.search_engine_entityscore)) tbl_keywords
                    JOIN
                    (SELECT
                       id                                                                AS keyword_id,
                       char_length(keyword) - char_length(replace(keyword, ' ', '')) + 1 AS total_keys,
                       regexp_split_to_table(keyword, ' ')                               AS key
                     FROM public.keywords_keywords
                     WHERE id IN (SELECT keyword_id
                                  FROM public.query_parser_querykeywordstore
                                  WHERE query_id = {query_id})) tbl_query_keywords
                      ON lower(tbl_keywords.key) = lower(tbl_query_keywords.key)
                  GROUP BY tbl_keywords.keyword_id, tbl_query_keywords.keyword_id
                  HAVING (avg(tbl_query_keywords.total_keys) = 1 AND count(tbl_keywords.key) = 1) OR (count(tbl_keywords.key) > 1) -- optimization
                  ) tbl_keyword_match
                 JOIN (SELECT
                         keyword_id,
                         power(2, score * 10) AS score,
                         sum(power(2, score * 10))
                         OVER ()              AS sum_all_scores
                       FROM public.query_parser_querykeywordstore
                       WHERE query_id = {query_id}) tbl_query_word_store
                   ON tbl_keyword_match.query_keyword_id = tbl_query_word_store.keyword_id
                 JOIN public.search_engine_entityscore tbl_entity_score
                   ON tbl_keyword_match.keyword_id = tbl_entity_score.keyword_id
               GROUP BY tbl_entity_score.entity_id) sq
          JOIN entities_entity tbl_entity
            ON sq.entity_id = tbl_entity.id;
        """.format(query_id=self.query_object.id)

        entity_scores = []
        with connection.cursor() as cursor:
            cursor.execute(query)

            headers = cursor.description
            range_min = 999999
            range_max = 0

            for row in cursor.fetchall():
                elem = {}
                if row[1] > search_constants.RESULT_THRESHOLD:
                    range_min = row[1] if row[1] < range_min else range_min
                    range_max = row[1] if row[1] > range_max else range_max
                    for index in range(0, len(headers)):
                        elem[headers[index][0]] = row[index]
                    # appending similarity score
                    elem['entity_similarity_score'] = similarity(self.query_object.text, row[0])
                    entity_scores.append(elem)

        # adding score combining logic and providing single score
        for elem in entity_scores:
            if not (range_max - range_min):
                normalized_entity_score = (elem['entity_score'] - range_min)
            else:
                normalized_entity_score = (elem['entity_score'] - range_min) / (range_max - range_min)
            elem['entity_score'] = normalized_entity_score * search_constants.LEXICAL_ANALYZER_WEIGHT + elem[
                'entity_similarity_score'] * search_constants.SEMANTIC_ANALYZER_WEIGHT

            elem.pop('entity_similarity_score', None)

        # Each element of entity_scores list is a dictionary with keys entity_id, entity_score and is like:
        # {
        #     'entity_id': '<entity_id>',
        #     'entity_score': '<entity_score'
        # }

        # Sort by score
        return sorted(entity_scores, key=itemgetter('entity_score'), reverse=True)
