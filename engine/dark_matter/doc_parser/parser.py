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

    WEIGHTS = {
        "local": 2,
        "global": 1
    }

    def __init__(self):
        self.documents = Document.objects.filter(is_parsed=False)
        self.normalized_weights = {}
        self.normalize_weights()

    def normalize_weights(self):
        """
        Normalize all weights to value between 0 to 1
        """

        total_sum = sum(self.WEIGHTS.values())
        self.normalized_weights = {key: round(value/(total_sum*1.0), 4) for (key, value) in self.WEIGHTS.iteritems()}

    def put_entity(self, document, entity):
        return Entity.objects.get_or_create(document=document, entity=entity)[0]

    def put_keyword(self, keyword):
        return Keywords.objects.get_or_create(keyword=keyword)[0]

    def put_entity_score(self, entity, keywords, global_keywords):

        for keyword_data in keywords:
            keyword_list = set()
            if keyword_data:

                keyword, local_score = keyword_data
                keyword_list.add(keyword)

                global_score = global_keywords.get(keyword, 0)

                # Weights
                local_weight = self.normalized_weights["local"]
                global_weight = self.normalized_weights["global"]

                EntityScore.objects.update_or_create(
                    entity=entity,
                    keyword=self.put_keyword(keyword),
                    defaults={
                        'score_document': {
                            "local_score": local_score,
                            "global_score": global_score,
                            "local_weight": local_weight,
                            "global_weight": global_weight
                        },
                        'score': self.calculate_score([local_score, global_score], [local_weight, global_weight])
                    }
                )

    def calculate_score(self, scores, weights):
        return sum([round(_score*_weight, 2) for (_score, _weight) in zip(scores, weights)])

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
        chunks = chunker.SmartSegmentChunker(file_content).chunk()

        processor = self.get_processor()

        # Global context information store in dict format
        global_annotations = dict(analyzer.DrakeAnalyzer(". ".join(chunks), processor).analyze())

        annotated_chunks = dict()

        # Analyze it
        for chunk in chunks:
            annotated_chunks[chunk] = analyzer.DrakeAnalyzer(chunk, processor).analyze()

        # Coalesce the entities
        annotated_entities = coalescer.DummyCoalesce(annotated_chunks).coalesce()

        for entity, keyword in annotated_entities.iteritems():
            entity_obj = self.put_entity(document, entity)
            self.put_entity_score(entity_obj, keyword, global_annotations)

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
