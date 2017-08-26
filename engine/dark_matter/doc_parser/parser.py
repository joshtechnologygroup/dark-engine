from __future__ import unicode_literals

from nltk import corpus

from dark_matter.commons import parser as commons_parser
from dark_matter.doc_parser import (
    analyzer,
    chunker,
    coalescer,
    converter as doc_converter
)
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

    def get_processor(self):
        stopwords = corpus.stopwords.words('english')
        return commons_parser.IndexingDrake(stopwords)

    def parse_document(self, document):
        """
        Parse Documents
        """

        # Get file stream
        file_content = doc_converter.TextDocConverter().process(document.file.url)

        # Chunk it
        chunks = chunker.SentenceChunker(file_content).chunk()

        processor = self.get_processor()

        # Analyze it
        for chunk in chunks:
            keywords = analyzer.DrakeAnalyzer(chunk, processor).analyze()

            # Coalesce it
            entity = coalescer.DummyCoalesce(chunk).coalesce()

            entity_obj = self.put_entity(document, entity)
            self.put_entity_score(entity_obj, keywords)

    def parse(self):
        """
        """

        for document in self.documents:
            self.parse_document(document)

        self.post_parse()

    def post_parse(self):
        self.documents.update(is_parsed=True)


if __name__ == 'doc_parser':
    DocParser().parse()
