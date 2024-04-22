from Procesamiento import Procesamiento
from Preprocesamineto import Preprocesamiento
import pytest


class TestEncontrarCoincidencias:
    def setup_method(self):
        self.procesamiento = Procesamiento()
        self.preprocesamiento = Preprocesamiento()

    #  Returns a list of dictionaries with 'cadena_orig', 'cadena_plag', and 'longitud' keys
    def test_returns_list_of_dictionaries(self):
        # Arrange
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is the plagiarized sentence"]

        # Act
        coincidencias = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        # Assert
        assert isinstance(coincidencias, list)
        for coincidencia in coincidencias:
            assert isinstance(coincidencia, dict)
            assert "cadena_orig" in coincidencia
            assert "cadena_plag" in coincidencia
            assert "longitud" in coincidencia

    #  Creates instances of Preprocesamiento class
    def test_creates_instances_of_Preprocesamiento_class(self, mocker):
        # Arrange
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is the plagiarized sentence"]
        mocker.patch.object(Preprocesamiento, 'get_stemmer', return_value="original plagiarized")

        # Act
        coincidencias = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        # Assert
        assert isinstance(coincidencias, list)
        for coincidencia in coincidencias:
            assert isinstance(coincidencia, dict)
            assert "cadena_orig" in coincidencia
            assert "cadena_plag" in coincidencia
            assert "longitud" in coincidencia

    #  No matches between original and plagiarized sentences
    def test_no_matches_between_sentences(self):
        # Arrange
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is a different sentence"]

        # Act
        coincidencias = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        # Assert
        assert len(coincidencias) == 0
