from django.core.management.base import BaseCommand

from dark_matter.entities.models import Document, Entity
from dark_matter.keywords.models import Keywords
from dark_matter.search_engine.models import EntityScore
from dark_matter.doc_parser.doc_parser import DocParser


class Command(BaseCommand):
    help = 'Parses the Documents'

    def handle(self, *args, **options):

        # Clear existing data
        Entity.objects.all().delete()
        Keywords.objects.all().delete()
        EntityScore.objects.all().delete()

        # Mark Back Document Parsing
        Document.objects.all().update(is_parsed=False)

        # Start Parse
        DocParser().parse()
