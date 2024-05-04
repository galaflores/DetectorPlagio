from gensim.models import Doc2Vec
from Procesamiento import Procesamiento

import pytest

class TestTrainDoc2vec:

    #  The method should raise an exception if an empty list of tagged documents is given.
    def test_empty_list_of_tagged_documents(self):
        # Arrange
        tagged_documents = []
    
        # Act
        procesamiento = Procesamiento()
    
        # Assert
        with pytest.raises(Exception):
            procesamiento.train_doc2vec(tagged_documents)

    #  The method should raise an exception if a list of tagged documents with empty documents is given.
    def test_list_of_tagged_documents_with_empty_documents(self):
        # Arrange
        tagged_documents = [("doc1", []),
                            ("doc2", []),
                            ("doc3", [])]
    
        # Act
        procesamiento = Procesamiento()
    
        # Assert
        with pytest.raises(Exception):
            procesamiento.train_doc2vec(tagged_documents)
