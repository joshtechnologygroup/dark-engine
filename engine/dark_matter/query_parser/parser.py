import RAKE
from nltk import corpus


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
