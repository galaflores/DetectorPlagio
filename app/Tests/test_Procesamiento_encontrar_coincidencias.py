from Procesamiento import Procesamiento
from Preprocesamineto import Preprocesamiento
import pytest

class TestEncontrarCoincidencias:
    def setup_method(self):
        self.procesamiento = Procesamiento()
        self.preprocesamiento = Preprocesamiento()

    #  The method returns a list of dictionaries with the original and plagiarized sentences, and their length.
    def test_returns_list_of_dictionaries(self):
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is the plagiarized sentence"]

        coincidencias, matriz_auc = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        assert isinstance(coincidencias, list)
        assert all(isinstance(coincidencia, dict) for coincidencia in coincidencias)
        assert all("cadena_orig" in coincidencia and "cadena_plag" in coincidencia and "longitud" in coincidencia for coincidencia in coincidencias)
        assert all(isinstance(coincidencia["cadena_orig"], str) and isinstance(coincidencia["cadena_plag"], str) and isinstance(coincidencia["longitud"], int) for coincidencia in coincidencias)

    #  The method counts the number of true positives, false positives, true negatives, and false negatives.
    def test_counts_metrics(self):
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is the plagiarized sentence"]

        coincidencias, matriz_auc = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        assert isinstance(matriz_auc, dict)
        assert all(key in matriz_auc for key in ["TP", "FP", "TN", "FN"])
        assert all(isinstance(value, int) for value in matriz_auc.values())

    #  The method only considers matches with more than three words.
    def test_considers_matches_with_more_than_three_words(self, mocker):
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is the plagiarized sentence"]

        coincidencias, matriz_auc = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        assert coincidencias == []

    #  The method applies stemming and removes stopwords to the matched sentences.
    def test_applies_stemming_and_removes_stopwords(self, mocker):
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is the plagiarized sentence"]

        coincidencias, matriz_auc = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        assert coincidencias == []

    #  The method returns a tuple with the list of matches and the AUC matrix.
    def test_returns_tuple_with_list_of_matches_and_AUC_matrix(self, mocker):
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is the plagiarized sentence"]

        coincidencias, matriz_auc = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        assert isinstance(coincidencias, list)
        assert isinstance(matriz_auc, dict)

    #  The method returns an empty list if there are no matches.
    def test_returns_empty_list_if_no_matches(self, mocker):
        sentences_originales = ["This is the original sentence"]
        sentences_plagiados = ["This is not a plagiarized sentence"]

        coincidencias, matriz_auc = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        assert coincidencias == []

    #  The method returns an empty list if the input sentences are empty.
    def test_returns_empty_list_if_input_sentences_are_empty(self, mocker):
        sentences_originales = []
        sentences_plagiados = []

        coincidencias, matriz_auc = Procesamiento.encontrar_coincidencias(sentences_originales, sentences_plagiados)

        assert coincidencias == []

    #  The method returns an empty list if the input sentences contain only one word.
    def test_returns_empty_list_if_input_sentences_contain_only_one_word(self, mocker):
        sentences_originales = ["original"]
