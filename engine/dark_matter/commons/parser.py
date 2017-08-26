# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator

from RAKE import RAKE
from nltk import word_tokenize, pos_tag, WordNetLemmatizer
from nltk.corpus.reader import wordnet as wordnet_reader

MAX_PHRASE_LENGTH_IN_SCORE = 4  # Consider maximum of these many words while calculating score
PHRASE_EXPONENTIAL_DECAY = 0.5  # Factor by which score importance of words decrease for phrase
WORD_LENGTH_BONUS_MODIFIER = 0.05


class DRAKE(RAKE.Rake):
    """
    Our own Custom RAKE Engine
    """

    def __init__(self, stop_words):
        """
        :param stop_words: Stop Words List [Array]
        """

        # We need to recalculate Stop words here also
        # since Rake internally stores result in __var which is annoying to access
        self.stop_words_pattern = RAKE.build_stop_word_regex(stop_words)
        self.word_list = dict()
        self.phrase_list = []
        super(DRAKE, self).__init__(stop_words)

    def generate_word_list(self):
        """
        Generate mapping for Word List for all phrases
        """

        for phrase in self.phrase_list:
            self.word_list[phrase] = RAKE.separate_words(phrase, 0)

    def calculate_word_scores(self):
        """
        Overwritten to normalize word scores.
        Can be extended to include Stemming and other features
        """

        word_frequency = {}
        word_degree = {}

        max_word_list_length = 1

        for phrase in self.phrase_list:
            word_list = self.word_list[phrase]
            word_list_length = len(word_list)

            if word_list_length > max_word_list_length:
                max_word_list_length = word_list_length

            word_list_degree = word_list_length - 1
            for word in word_list:
                word_frequency.setdefault(word, 0)
                word_frequency[word] += 1
                word_degree.setdefault(word, 0)
                word_degree[word] += word_list_degree

        for item in word_frequency:
            word_degree[item] = word_degree[item] + word_frequency[item]

        # Calculate Word scores = deg(w)/freq(w)
        word_score = {}
        for item in word_frequency:
            word_score.setdefault(item, 0)
            word_score[item] = (word_degree[item] / (word_frequency[item] * 1.0)) / max_word_list_length

        return word_score

    def generate_candidate_word_scores(self, word_score):
        """
        Overwritten to normalize candidate scores
        Traditional Version: All word scores are added up to give final score

        Our Version:
            We say Highest_word_score*1.0 + next_highest*0.5 + next*0.25 + next*0.125 (All other entries ignored)
            Divided by (1.0 + .5 + .25 + .125)

            After this we multiply by WORD_LENGTH_MODIFIER (capping it at 4 words)
        """

        keyword_candidates = {}

        for phrase in self.phrase_list:
            keyword_candidates.setdefault(phrase, 0)
            word_list = self.word_list[phrase]

            candidate_scores = []

            for word in word_list:
                candidate_scores.append(word_score[word])

            candidate_score = 0

            # Normalize candidate score
            normalization_parameter = 0
            for idx, c_score in enumerate(sorted(candidate_scores, reverse=True)[:MAX_PHRASE_LENGTH_IN_SCORE]):
                decay_factor = PHRASE_EXPONENTIAL_DECAY ** idx
                normalization_parameter += decay_factor
                candidate_score += (c_score * decay_factor)

            if normalization_parameter:
                candidate_score /= normalization_parameter

            # Add bonus for word length
            word_length_bonus_modifier = 1 + min(
                len(candidate_scores) - 1, MAX_PHRASE_LENGTH_IN_SCORE
            ) * WORD_LENGTH_BONUS_MODIFIER
            candidate_score = min(round(candidate_score * word_length_bonus_modifier, 2), 1.0)

            keyword_candidates[phrase] = candidate_score

        return keyword_candidates

    def pre_process(self, text):
        tokens = word_tokenize(text)
        tagged_tokens = pos_tag(tokens)
        return self.lemmatize(tagged_tokens)

    def lemmatize(self, tagged_tokens):
        """
        Lemmatization Code
        :param text: dict of phrases with scores as values
        :param tagged_tokens: tokens with their pos
        :return:
        """

        lemmatized_text = ''
        for word, tag in tagged_tokens:
            if tag.startswith('J'):
                wordnet_tag = wordnet_reader.ADJ
            elif tag.startswith('V'):
                wordnet_tag = wordnet_reader.VERB
            elif tag.startswith('N'):
                wordnet_tag = wordnet_reader.NOUN
            elif tag.startswith('R'):
                wordnet_tag = wordnet_reader.ADV
            else:
                wordnet_tag = wordnet_reader.NOUN
            lemmatized_text = lemmatized_text + ' ' + WordNetLemmatizer().lemmatize(word, wordnet_tag)
        return lemmatized_text

    def run(self, text):
        lemmatized_text = self.pre_process(text)
        sentence_list = RAKE.split_sentences(lemmatized_text)

        self.phrase_list = RAKE.generate_candidate_keywords(sentence_list, self.stop_words_pattern)
        self.generate_word_list()

        word_scores = self.calculate_word_scores()

        keyword_candidates = self.generate_candidate_word_scores(word_scores)

        sorted_keywords = sorted(keyword_candidates.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords


class IndexingDrake(DRAKE):
    """
    DRAKE used by Indexing Engine
    """


class QueryNLPDrake(DRAKE):
    """
    DRAKE user by Query Parser Engine
    """
