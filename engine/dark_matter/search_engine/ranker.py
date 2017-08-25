from operator import itemgetter

from django.db.models import Count, Avg
from django.db import connection

from dark_matter.search_engine import (
    constants as search_constants,
    models as search_models
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
            tbl_entity.entity_id,
            sum(tbl_entity.score * tbl_query.score) / avg(sum_all_scores) AS entity_score
        FROM public.search_engine_entityscore tbl_entity
            JOIN (SELECT
                        keyword_id,
                        score,
                        sum(score) OVER (PARTITION BY keyword_id) AS sum_all_scores
                    FROM public.query_parser_querykeywordstore
                    WHERE query_id = {query_id}) tbl_query
                ON tbl_entity.keyword_id = tbl_query.keyword_id
        GROUP BY tbl_entity.entity_id;

        """.format(query_id=self.query_id)

        entity_scores = []
        with connection.cursor() as cursor:
            cursor.execute(query)

            headers = cursor.description

            for row in cursor.fetchall():
                elem = {}
                for index in range(0, headers):
                    elem[headers[index]] = row[index]}
                entity_scores.append(elem)

        # Each element of entity_scores list is a dictionary with keys entity_id, entity_score and is like:
        # {
        #     'entity_id': '<entity_id>',
        #     'entity_score': '<entity_score'
        # }

        # Sort by score
        return sorted(entity_scores, key=itemgetter("entity_score"), reverse=True)
