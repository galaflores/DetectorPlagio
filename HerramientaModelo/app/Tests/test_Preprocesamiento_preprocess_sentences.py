from gensim.models.doc2vec import TaggedDocument
from Preprocesamineto import Preprocesamiento

import pytest

class TestPreprocessSentences:

    #  The method should correctly tokenize the input sentences.
    def test_tokenize_sentences(self):
        sentences = ["This is the first sentence.", "And this is the second sentence."]
        preprocessor = Preprocesamiento()
        tagged_sentences = preprocessor.preprocess_sentences(sentences)
        assert len(tagged_sentences) == 2
        assert tagged_sentences[0].words == ['this', 'is', 'the', 'first', 'sentence']
        assert tagged_sentences[1].words == ['and', 'this', 'is', 'the', 'second', 'sentence']


    #  The method should correctly tag each sentence with a unique identifier.
    def test_tag_sentences(self):
        sentences = ["This is the first sentence.", "And this is the second sentence."]
        preprocessor = Preprocesamiento()
        tagged_sentences = preprocessor.preprocess_sentences(sentences)
        assert len(tagged_sentences) == 2
        assert tagged_sentences[0].tags == ['0']
        assert tagged_sentences[1].tags == ['1']

    #  The method should return a list of TaggedDocument objects.
    def test_return_tagged_documents(self):
        sentences = ["This is the first sentence.", "And this is the second sentence."]
        preprocessor = Preprocesamiento()
        tagged_sentences = preprocessor.preprocess_sentences(sentences)
        assert isinstance(tagged_sentences, list)
        assert all(isinstance(tagged_sentence, TaggedDocument) for tagged_sentence in tagged_sentences)

    #  The input sentences list is empty.
    def test_empty_sentences_list(self):
        sentences = []
        preprocessor = Preprocesamiento()
        tagged_sentences = preprocessor.preprocess_sentences(sentences)
        assert tagged_sentences == []

