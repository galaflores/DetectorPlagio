from app.Preprocesamineto import Preprocesamiento
import pytest


class TestBuscarYTokenizar:

    #  Returns an empty list when given an invalid filename.
    def test_invalid_filename(self, mocker):
        # Mock the os.listdir() method to return a list with a different filename
        mocker.patch('os.listdir', return_value=['otherfile.txt'])

        # Call the method under test
        result = Preprocesamiento.buscar_y_tokenizar('directory', 'filename.txt')

        # Assert that the result is an empty list
        assert result == []

    #  Returns an empty list when given an invalid directory.
    def test_invalid_directory(self, mocker):
        # Mock the os.listdir() method to return an empty list
        mocker.patch('os.listdir', return_value=[])

        # Call the method under test
        result = Preprocesamiento.buscar_y_tokenizar('directory', 'filename.txt')

        # Assert that the result is an empty list
        assert result == []