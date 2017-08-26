# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nltk import corpus

from dark_matter.commons import parser as commons_parser
from dark_matter.doc_parser.doc_converter import DocConverter
from dark_matter.entities.models import Document, Entity
from dark_matter.keywords.models import Keywords
from dark_matter.search_engine.models import EntityScore


class DocParser(object):
    """
    Parse documents and extract keywords entities and relations between then

    Currently, we parse all documents at one go.
    We could later turn this into batch processing module if list grows big enough
    """

    # TODO: We may be able to bulk-insert Keywords, Entities and Scores to improve performance

    def __init__(self):
        self.documents = Document.objects.filter(is_parsed=False)

    def put_entity(self, document, entity):
        return Entity.objects.get_or_create(document=document, entity=entity)[0]

    def put_keyword(self, keyword):
        return Keywords.objects.get_or_create(keyword=keyword)[0]

    def put_entity_score(self, entity, keywords):
        for keyword_data in keywords:
            if keyword_data:
                keyword, score = keyword_data
                EntityScore.objects.update_or_create(
                    entity=entity,
                    keyword=self.put_keyword(keyword),
                    defaults={'score': score}
                )

    def extract_keywords(self, sentence, processor):
        """
        Extract Keywords and assign score to them for each sentence
        """
        return processor.run(sentence)

    def get_processor(self):
        stopwords = corpus.stopwords.words('english')
        return commons_parser.IndexingDrake(stopwords)

    def parse_document(self, document):
        """
        Parse Documents
        """

        file_content = DocConverter().convert(document.file.url)
        processor = self.get_processor()
        for sentence in file_content:
            keywords = self.extract_keywords(sentence, processor)

            entity = self.put_entity(document, sentence)
            self.put_entity_score(entity, keywords)

    def parse(self):
        """
        :return:
        """

        for document in self.documents:
            self.parse_document(document)

        self.post_parse()

    def post_parse(self):
        self.documents.update(is_parsed=True)


if __name__ == 'doc_parser':
    DocParser().parse()
