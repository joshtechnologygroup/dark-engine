from operator import itemgetter

from django.db import connection

from dark_matter.search_engine import (
    constants as search_constants,
)


class Ranker(object):

    def __init__(self, query_id):
        """
        Expected that query_id will be of Integer Type representing ID of the query running
        """

        self.query_id = query_id

    def processor(self):
        """
        Basic processor which only needs List of Keywords to operate on
        """

        query = """
        SELECT
          tbl_entity.entity AS entity_text,
          sq.entity_score
        FROM (
        SELECT
          tbl_entity_score.entity_id,
          sum(tbl_entity_score.score * tbl_query.score) / avg(sum_all_scores) AS entity_score
        FROM public.search_engine_entityscore tbl_entity_score
          JOIN (SELECT
                  keyword_id,
                  power(2, score*10) as score,
                  sum(power(2, score*10)) OVER () AS sum_all_scores
                FROM public.query_parser_querykeywordstore
                WHERE query_id = '{query_id}') tbl_query
            ON tbl_entity_score.keyword_id = tbl_query.keyword_id
        GROUP BY tbl_entity_score.entity_id) sq
          JOIN entities_entity tbl_entity
            ON sq.entity_id = tbl_entity.id;
        """.format(query_id=self.query_id)

        entity_scores = []
        with connection.cursor() as cursor:
            cursor.execute(query)

            headers = cursor.description

            for row in cursor.fetchall():
                elem = {}
                if row[1] > search_constants.RESULT_THRESHOLD:
                    for index in range(0, len(headers)):
                        elem[headers[index][0]] = row[index]
                    entity_scores.append(elem)

        # Each element of entity_scores list is a dictionary with keys entity_id, entity_score and is like:
        # {
        #     'entity_id': '<entity_id>',
        #     'entity_score': '<entity_score'
        # }

        # Sort by score
        return sorted(entity_scores, key=itemgetter("entity_score"), reverse=True)
