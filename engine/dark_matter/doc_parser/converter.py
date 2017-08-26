from os.path import join

from django.conf import settings


class DocConverter(object):
    """
    Converts Document from one format to standard text stream
    """

    def __init__(self):
        self.content = None

    def process(self, file_name):
        self.load_file(file_name)
        return self.convert()

    def load_file(self, file_name):
        with open(join(settings.DJANGO_ROOT, file_name), str('r')) as document_file:
            self.content = document_file.readlines()

    def convert(self):
        raise NotImplemented


class TextDocConverter(DocConverter):
    """
    Handles simple text files
    """

    def convert(self):
        return " ".join(self.content)
