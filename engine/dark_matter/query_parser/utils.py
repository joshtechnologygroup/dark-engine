import math

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
