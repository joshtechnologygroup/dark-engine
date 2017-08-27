from collections import defaultdict

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

    # TODO: Use constants for Global, local, tags etc

    WEIGHTS = {
        "local": 3,
        "global": 1,
        "tags": 1
        # TODO: Tags are special as in if they are present, they should have score,
        # TODO: But if not present, should not penalize other feedback loops
    }

    def __init__(self):
        self.documents = Document.objects.filter(is_parsed=False)
        self.normalized_weights = {}
        self.normalize_weights()

        # Keep adding weighted scores here
        self.weighted_scores = defaultdict(dict)

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

    def put_entity_score(self, entity):

        # Weights
        local_weight = self.normalized_weights["local"]
        global_weight = self.normalized_weights["global"]
        tags_weight = self.normalized_weights["tags"]

        for keyword in self.weighted_scores:
            local_score = self.weighted_scores[keyword].get("local", 0)
            global_score = self.weighted_scores[keyword].get("global", 0)
            tags_score = self.weighted_scores[keyword].get("tags", 0)

            EntityScore.objects.update_or_create(
                entity=entity,
                keyword=self.put_keyword(keyword),
                defaults={
                    'score_document': {
                        "local_score": local_score,
                        "global_score": global_score,
                        "local_weight": local_weight,
                        "global_weight": global_weight,
                        "tags_score": tags_score,
                        "tags_weight": tags_weight
                    },
                    'score': self.calculate_score(
                        [local_score, global_score, tags_score],
                        [local_weight, global_weight, tags_weight]
                    )
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
        keyword_dict = dict(analyzer.DrakeAnalyzer(". ".join(chunks), processor).analyze())
        for key, value in keyword_dict.iteritems():
            self.weighted_scores[key]["global"] = value

        # Tags information
        for key in document.tags.all():
            self.weighted_scores[key]["tags"] = 1

        annotated_chunks = dict()

        # Analyze it
        for chunk in chunks:
            annotated_chunks[chunk] = analyzer.DrakeAnalyzer(chunk, processor).analyze()

        # Coalesce the entities
        annotated_entities = coalescer.DummyCoalesce(annotated_chunks).coalesce()

        local_keys = set()
        for entity, keywords in annotated_entities.iteritems():
            entity_obj = self.put_entity(document, entity)

            # Clear previous local keys
            self.clear_local_keys(local_keys)
            local_keys = set()

            # Assign for this round
            for key, score in keywords:
                local_keys.add(key)
                self.weighted_scores[key]["local"] = score

            self.put_entity_score(entity_obj)

    def clear_local_keys(self, local_keys):
        for key in self.weighted_scores:
            if key in local_keys:
                del self.weighted_scores[key]["local"]

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
