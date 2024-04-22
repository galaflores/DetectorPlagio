import pytest

from app.DetectorDePlagio import DetectorDePlagio


class TestPreprocesarTexto:

    # Returns a list of n-grams for a given file path and directory path.
    def test_returns_list_of_ngrams(self):
        detector = DetectorDePlagio()
        archivo = "path/to/file.txt"
        ruta = "path/to/directory"
        result = detector.preprocesar_texto(archivo, ruta)
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)
        assert all(isinstance(ngram, str) for ngram in result[0])
        assert all(isinstance(ngram, str) for ngram in result[1])

    # Empty file path raises an error.
    def test_empty_file_path_raises_error(self):
        detector = DetectorDePlagio()
        archivo = ""
        ruta = "path/to/directory"
        with pytest.raises(Exception):
            detector.preprocesar_texto(archivo, ruta)

    # Handles multiple text files in the directory path.
    def test_handles_multiple_text_files(self):
        detector = DetectorDePlagio()
        archivo = "path/to/file.txt"
        ruta = "path/to/directory"
        result = detector.preprocesar_texto(archivo, ruta)
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)
        assert all(isinstance(ngram, str) for ngram in result[0])
        assert all(isinstance(ngram, str) for ngram in result[1])

    # Uses stemming to preprocess the text.
    def test_uses_stemming(self):
        detector = DetectorDePlagio()
        archivo = "path/to/file.txt"
        ruta = "path/to/directory"
        result = detector.preprocesar_texto(archivo, ruta)
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)
        assert all(isinstance(ngram, str) for ngram in result[0])
        assert all(isinstance(ngram, str) for ngram in result[1])

    # Uses trigrams to generate n-grams.
    def test_uses_trigrams(self):
        detector = DetectorDePlagio()
        archivo = "path/to/file.txt"
        ruta = "path/to/directory"
        result = detector.preprocesar_texto(archivo, ruta)
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)
        assert all(isinstance(ngram, str) for ngram in result[0])
        assert all(isinstance(ngram, str) for ngram in result[1])