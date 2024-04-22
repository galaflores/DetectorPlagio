from Data import Data
from nltk.stem import LancasterStemmer
import re
import os
import pytest


class TestGetStemmer:

    #  The method receives a string as input and returns a string as output.
    def test_string_input_returns_string_output(self):
        # Arrange
        data = Data()
        texto = "This is a test string"
        expected_output = "thi is a test string"

        # Act
        result = data.get_stemmer(texto)

        # Assert
        assert isinstance(result, str)
        assert result == expected_output

    #  The method receives an empty string as input and returns an empty string as output.
    def test_empty_string_input_returns_empty_string_output(self):
        # Arrange
        data = Data()
        texto = ""
        expected_output = ""

        # Act
        result = data.get_stemmer(texto)

        # Assert
        assert isinstance(result, str)
        assert result == expected_output
