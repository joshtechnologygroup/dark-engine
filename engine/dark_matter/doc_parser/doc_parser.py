import RAKE
from nltk import corpus

from dark_matter.doc_parser.doc_converter import DocConverter
from dark_matter.entities.models import Document, Entity
from dark_matter.keywords.models import Keywords
from dark_matter.search_engine.models import EntityScore


class DocParser(object):
    """
    Parse Documentation to get entities
    """

    def get_documents(self):
        """
        Get all documents which have not been parsed yet
        """
        return Document.objects.filter(is_parsed=False)

    def put_entity(self, document, entity):
        return Entity.objects.get_or_create(document=document, entity=entity)[0]

    def put_keyword(self, keyword):
        return Keywords.objects.get_or_create(keyword=keyword)[0]

    def put_entity_score(self, entity, keywords):
        for keyword_data in keywords:
            if keyword_data:
                keyword, score = keyword_data
                EntityScore.objects.get_or_create(
                    entity=entity,
                    keyword=self.put_keyword(keyword),
                    score=score
                )

    def extract_keywords(self, sentance):
        """"""
        stopwords = corpus.stopwords.words('english')
        rake = RAKE.Rake(stopwords)

        max_weight = 0
        keywords_with_weight = rake.run(sentance)

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

    def parse_document(self, document):
        """"""
        file_content = DocConverter().convert(document.file.url)
        for sentence in file_content:
            keywords = self.extract_keywords(sentence)

            entity = self.put_entity(document, sentence)
            self.put_entity_score(entity, keywords)

    def parse(self):
        """"""
        documents = self.get_documents()

        for document in documents:
            self.parse_document(document)


if __name__ == 'doc_parser':
    DocParser().parse()
