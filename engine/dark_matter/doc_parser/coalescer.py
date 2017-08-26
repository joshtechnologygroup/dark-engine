class Coalesce(object):
    """
    Coalesce meaningful chunks together
    """

    def __init__(self, annotated_chunks):
        """
        :param annotated_chunks: dict
        {
            chunk1: metadata,
            chunk2: metadata,
            ...
        }
        """
        self.annotated_chunks = annotated_chunks

    def coalesce(self):
        raise NotImplemented


class DummyCoalesce(Coalesce):
    """
    Does nothing and return the chunks as it is
    """

    def coalesce(self):
        return self.annotated_chunks
