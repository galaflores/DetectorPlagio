from TiposDePlagio import TiposDePlagio

import pytest

class TestDetectarParafraseo:

    #  Returns True if the similarity ratio between the original and plagiarized sentences is equal to the specified threshold
    def test_similarity_ratio_equal_threshold(self):
        original_sentence = "The cat is on the mat."
        plagiarized_sentence = "The cat is on the mat."
        threshold = 0.8

        result = TiposDePlagio.detectar_parafraseo(original_sentence, plagiarized_sentence, threshold)

        assert result is True

    #  Returns False if either the original or plagiarized sentence is empty
    def test_empty_sentence(self):
        original_sentence = ""
        plagiarized_sentence = "The cat is on the mat."

        result = TiposDePlagio.detectar_parafraseo(original_sentence, plagiarized_sentence)

        assert result is False

    #  Returns True if the original and plagiarized sentences are identical
    def test_identical_sentences(self):
        original_sentence = "The cat is on the mat."
        plagiarized_sentence = "The cat is on the mat."

        result = TiposDePlagio.detectar_parafraseo(original_sentence, plagiarized_sentence)

        assert result is True


    #  Returns False if the original sentence is a subset of the plagiarized sentence
    def test_original_subset_of_plagiarized(self):
        original_sentence = "The cat is on the mat."
        plagiarized_sentence = "The cat is on the mat and the dog is on the mat."

        result = TiposDePlagio.detectar_parafraseo(original_sentence, plagiarized_sentence)

        assert result is False

    #  Returns False if the original and plagiarized sentences have no common words
    def test_no_common_words(self):
        original_sentence = "The cat is on the mat."
        plagiarized_sentence = "The dog is under the table."

        result = TiposDePlagio.detectar_parafraseo(original_sentence, plagiarized_sentence)

        assert result is False

    #  Returns True if the original and plagiarized sentences have only one word that is different
    def test_one_word_difference(self):
        original_sentence = "The cat is on the mat."
        plagiarized_sentence = "The cat is under the mat."

        result = TiposDePlagio.detectar_parafraseo(original_sentence, plagiarized_sentence)

        assert result is True
