import math

import RAKE
from nltk import (data, corpus, WordNetLemmatizer, Counter)


# stretch 1
def process_document(self, documents):
    tokenizer = data.load('tokenizers/punkt/english.pickle')
    lemmatizer = WordNetLemmatizer()
    stopwords = corpus.stopwords.words('english')
    tf = []  # term frequency
    idf = []
    tokens_list_doc_wise = []
    all_tokens = set()

    for document in documents:
        tokens = tokenizer.tokenize(document)
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        tokens = [token for token in tokens if token not in stopwords]
        tokens_list_doc_wise.append(tokens)
        tf.append(Counter(tokens))
        all_tokens.union(tokens)

    # calculating idf
    for token in all_tokens:
        present_in_documents = 0
        for x in range(0, len(documents)):
            present_in_documents += 1 if tf[x][token] > 0 else present_in_documents
        idf[token] = math.log(len(documents) / len(present_in_documents))

    # calculating tf_idf for tokens document wise
    tf_idf = []
    for x in range(0, len(tokens_list_doc_wise)):
        for token in tokens_list_doc_wise[x]:
            tf_idf[token] = tf[x][token] * idf[token]
            # persist to db tf_idf


# stretch 2
# def process_previous_queries(self):


def parse_query(query):
    stopwords = corpus.stopwords.words('english')
    rake = RAKE.Rake(stopwords)

    max_weight = 0
    keywords_with_weight = rake.run(query)
    for x in keywords_with_weight:
        if x[1] > max_weight:
            max_weight = x[1]

    normalized_keywords_with_weight = []
    for x in keywords_with_weight:
        normalized_keywords_with_weight.append((x[0], x[1] / max_weight))
    return normalized_keywords_with_weight
