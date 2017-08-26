class BaseAnalyzer(object):
    """
    Analyze the object and construct meaningful metadata from it
    """

    def __init__(self, text, *args, **kwargs):
        self.text = text

    def analyze(self):
        raise NotImplemented


class DrakeAnalyzer(BaseAnalyzer):
    """
    Analyzer based on our custom DRAKE Scores.
    It simple return list of Keywords which belong to this chunks
    """

    def __init__(self, text, processor, *args, **kwargs):
        self.processor = processor
        super(DrakeAnalyzer, self).__init__(text, *args, **kwargs)

    def analyze(self):
        return self.processor.run(self.text)
