from app.Preprocesamineto import Preprocesamiento
import pytest


class TestGetStemmer:
    def setup_method(self):
        self.preprocesamiento = Preprocesamiento()

    #  Returns a string with all stopwords removed and all words stemmed using LancasterStemmer.
    def test_remove_stopwords_and_stem_words(self):
        # Arrange
        texto = "This is a sample text with stopwords"
        expected_result = "sampl text stopword"

        # Act
        result = self.preprocesamiento.get_stemmer(texto)

        # Assert
        assert result == expected_result

    #  Returns an empty string when given an empty string.
    def test_empty_string_input(self):
        # Arrange
        texto = ""
        expected_result = ""

        # Act
        result = self.preprocesamiento.get_stemmer(texto)

        # Assert
        assert result == expected_result

    # Returns a string with all stopwords removed and all words stemmed using LancasterStemmer, even when input has
    # mixed case.
    def test_mixed_case_input(self):
        # Arrange
        texto = "This is a Sample Text with Stopwords"
        expected_result = "sampl text stopword"

        # Act
        result = self.preprocesamiento.get_stemmer(texto)

        # Assert
        assert result == expected_result

    # Returns a string with all stopwords removed and all words stemmed using LancasterStemmer, even when input has
    # only one word.
    def test_single_word_input(self):
        # Arrange
        texto = "sample"
        expected_result = "sampl"

        # Act
        result = self.preprocesamiento.get_stemmer(texto)

        # Assert
        assert result == expected_result

    # Returns a string with all stopwords removed and all words stemmed using LancasterStemmer, even when input has
    # only one stopword.
    def test_single_stopword_input(self):
        # Arrange
        texto = "this"
        expected_result = ""

        # Act
        result = self.preprocesamiento.get_stemmer(texto)

        # Assert
        assert result == expected_result

    # Returns a string with all stopwords removed and all words stemmed using LancasterStemmer, even when input has
    # only one character.
    def test_single_character_input(self):
        # Arrange
        texto = "a"
        expected_result = ""

        # Act
        result = self.preprocesamiento.get_stemmer(texto)

        # Assert
        assert result == expected_result
