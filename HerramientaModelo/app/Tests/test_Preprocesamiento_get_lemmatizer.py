from unittest.mock import Mock
from Preprocesamineto import Preprocesamiento
import pytest

class TestGetLemmatizer:
    #  Handles input with only non-alphabetic characters
    def test_lemmatizer_with_only_non_alphabetic_characters(self):
        # Arrange
        mocker = Mock()
        preprocesamiento = Preprocesamiento()
        preprocesamiento.remove_stopwords = mocker.Mock(return_value="!@#$%^&*()")
        preprocesamiento.get_lemmatizer = mocker.Mock(return_value="!@#$%^&*()")
        text = "!@#$%^&*()"
    
        # Act
