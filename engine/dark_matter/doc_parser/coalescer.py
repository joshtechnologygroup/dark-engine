class Coalesce(object):
    """
    Coalesce meaningful chunks together
    """

    def __init__(self, annotated_chunks):
        self.chunks = annotated_chunks

    def coalesce(self):
        raise NotImplemented


class DummyCoalesce(Coalesce):
    """
    Does nothing and return as it is
    """

    def coalesce(self):
        return self.chunks
