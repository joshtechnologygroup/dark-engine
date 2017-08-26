from os.path import join

import nltk
from django.conf import settings


class DocConverter(object):
    """"""

    def load_file(self, file_name):
        """"""
        with open(join(settings.DJANGO_ROOT, file_name), 'r') as document_file:
            lines = document_file.readlines()

        return " ".join(lines).replace('\n', '').replace('\r', '')

    def split_sentences(self, file_content):
        """"""
        return nltk.sent_tokenize(file_content)

    def convert(self, file_name):
        file_content = self.load_file(file_name)

        return self.split_sentences(file_content)
