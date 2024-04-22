import pytest

class TestDetectPlagiarism:

    # selects a file and calls preprocesar_texto from DetectorDePlagio
    def test_selects_file_and_calls_preprocesar_texto(self):
        # Arrange
        app = App()
        file_path = "test_file.txt"
    
        # Act
        app.detect_plagiarism(file_path)
    
        # Assert
        # TODO: Add assertions

    # selects a non-existent file and returns an error message
    def test_selects_nonexistent_file_and_returns_error_message(self):
        # Arrange
        app = App()
        file_path = "nonexistent_file.txt"
    
        # Act
        app.detect_plagiarism(file_path)
    
        # Assert
        # TODO: Add assertions