from gensim.models import Doc2Vec
from Procesamiento import Procesamiento

# Dependencies:
# pip install pytest-mock
import pytest

class TestCalculateSimilarityDoc2vec:

    #  The method raises an exception if one or both documents are empty.
    def test_raises_exception_for_empty_documents(self, mocker):
        # Arrange
        doc1 = ""
        doc2 = "This is document 2"
        model = mocker.Mock(Doc2Vec)

        # Act & Assert
        with pytest.raises(Exception):
            self.calculate_similarity_doc2vec(doc1, doc2, model)





