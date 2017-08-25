from django.core.files import File

from dark_matter.doc_parser.doc_converter import DocConverter
from dark_matter.entities.models import Document, Entity
from dark_matter.keywords.models import Keywords
from dark_matter.query_parser.parser import Parser
from dark_matter.search_engine.models import EntityScore


class DocParser(object):
    """"""

    def get_documents(self):
        """"""
        return Document.objects.all()

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

    def parse_document(self, document):
        """"""
        file_content = DocConverter().convert(document.file.url)

        for sentence in file_content.split('.'):
            keywords = Parser(sentence).extract_keywords()

            entity = self.put_entity(document, sentence)
            self.put_entity_score(entity, keywords)

    def parse(self):
        """"""
        documents = self.get_documents()

        for document in documents:
            self.parse_document(document)


if __name__ == 'doc_parser':
    DocParser().parse()
