from Preprocesamineto import Preprocesamiento
import pytest


class TestRemoveStopwords:

    #  The method correctly removes all stopwords from the input text.
    def test_remove_stopwords_removes_all_stopwords(self):
        # Arrange
        text = "This is a sample text with stopwords"
        expected_result = "sample text stopwords"

        # Act
        result = Preprocesamiento.remove_stopwords(text)

        # Assert
        assert result == expected_result

    #  The method returns a string with all words in lowercase.
    def test_remove_stopwords_returns_lowercase_string(self):
        # Arrange
        text = "This is a Sample Text"
        expected_result = "sample text"

        # Act
        result = Preprocesamiento.remove_stopwords(text)

        # Assert
        assert result == expected_result

    #  The method correctly handles an empty string as input.
    def test_remove_stopwords_handles_empty_string(self):
        # Arrange
        text = ""
        expected_result = ""

        # Act
        result = Preprocesamiento.remove_stopwords(text)

        # Assert
        assert result == expected_result

    #  The method correctly handles a string with only one word as input.
    def test_remove_stopwords_handles_string_with_only_one_word(self):
        # Arrange
        text = "word"
        expected_result = "word"

        # Act
        result = Preprocesamiento.remove_stopwords(text)

        # Assert
        assert result == expected_result
