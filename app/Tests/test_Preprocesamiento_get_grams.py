from app.Preprocesamineto import Preprocesamiento

import pytest


class TestGetGrams:
    def setup_method(self):
        self.preprocesamiento = Preprocesamiento()

    #  Returns an empty list when given an empty string.
    def test_returns_empty_list_with_empty_string(self):
        # Arrange
        texto = ""
        ngram_number = 2
        expected_result = []

        # Act
        result = self.preprocesamiento.get_grams(texto, ngram_number)

        # Assert
        assert result == expected_result

    #  Returns an empty list when given a string with only special characters and numbers.
    def test_returns_empty_list_with_special_characters_and_numbers(self):
        # Arrange
        texto = "!@#$%^&*()1234567890"
        ngram_number = 3
        expected_result = []

        # Act
        result = self.preprocesamiento.get_grams(texto, ngram_number)

        # Assert
        assert result == expected_result

    #  Returns an empty list when given a string with only stopwords.
    def test_returns_empty_list_with_stopwords(self):
        # Arrange
        texto = "this is a with"
        ngram_number = 2
        expected_result = []

        # Act
        result = self.preprocesamiento.get_grams(texto, ngram_number)

        # Assert
        assert result == expected_result

    #  Returns an empty list when n-gram number is less than 1.
    def test_returns_empty_list_with_ngram_number_less_than_1(self):
        # Arrange
        texto = "This is a test sentence"
        ngram_number = 0
        expected_result = []

        # Act
        result = self.preprocesamiento.get_grams(texto, ngram_number)

        # Assert
        assert result == expected_result

    #  Returns an empty list when n-gram number is greater than the number of words in the text.
    def test_returns_empty_list_with_ngram_number_greater_than_number_of_words(self):
        # Arrange
        texto = "This is a test sentence"
        ngram_number = 6
        expected_result = []

        # Act
        result = self.preprocesamiento.get_grams(texto, ngram_number)

        # Assert
        assert result == expected_result
