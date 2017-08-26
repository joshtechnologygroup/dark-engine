import nltk


class BaseChunker(object):
    """
    Chunks the document into meaningful entities
    """

    def __init__(self, text):
        self.text = text

    def chunk(self):
        raise NotImplemented


class SentenceChunker(BaseChunker):
    """
    Chunks into sentences
    """

    def chunk(self):
        return nltk.sent_tokenize(self.text)


class ParagraphChunker(BaseChunker):
    """
    Chunks into Paragraphs
    """

    def chunk(self):
        return [line for line in self.text.splitlines() if line.strip()]
