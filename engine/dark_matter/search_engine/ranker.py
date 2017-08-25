from operator import itemgetter

from django.db.models import Count, Avg

from dark_matter.search_engine import (
    constants as search_constants,
    models as search_models
)


class Ranker(object):

    def __init__(self, keywords):

        self.keywords = keywords

    def processor(self):
        """
        Basic processor which only needs List of Keywords to operate on
        """

        qs_result = search_models.EntityScore.objects.filter(
            keyword__keyword__in=self.keywords
        ).values('entity').annotate(
            Count('keyword'), Avg('score')
        ).values_list(
            'entity__entity', 'keyword__count', 'score__avg'
        )

        kw_scores = []
        total_keywords = len(self.keywords)

        # Find Proportionate Rank
        # Score is Avg Score * Fraction of Keywords found in document
        for entity, keyword_count, avg_score in qs_result:
            score = avg_score*(keyword_count/(total_keywords*1.0))
            if score > search_constants.RESULT_THRESHOLD:
                kw_scores.append({
                    "answer": entity,
                    "score": score
                })

        # Sort by score
        return sorted(kw_scores, key=itemgetter("score"), reverse=True)
