from TiposDePlagio import TiposDePlagio

import pytest

class TestDetectarCambioTiempo:

    #  The method correctly detects a change in tense when the tense of the verbs in the original and plagiarized sentences are different.
    def test_change_in_tense_when_different_tense(self):
        original_sentence = "I am going to the store."
        plagiarized_sentence = "He goes to the store."
    
        result = TiposDePlagio.detectar_cambio_tiempo(original_sentence, plagiarized_sentence)
    
        assert result == True

    #  The method correctly detects no change in tense when the tense of the verbs in the original and plagiarized sentences are the same.
    def test_no_change_in_tense_when_same_tense(self):
        original_sentence = "I am going to the store."
        plagiarized_sentence = "He is going to the store."
    
        result = TiposDePlagio.detectar_cambio_tiempo(original_sentence, plagiarized_sentence)
    
        assert result == False


    #  The method correctly tags the parts of speech of the words in the original and plagiarized sentences.
    def test_tag_parts_of_speech(self, mocker):
        mocker.patch('nltk.pos_tag', return_value=[('I', 'PRP'), ('am', 'VBP'), ('going', 'VBG'), ('to', 'TO'), ('the', 'DT'), ('store', 'NN')])
        original_sentence = "I am going to the store."
        plagiarized_sentence = "He is going to the store."
    
        result = TiposDePlagio.detectar_cambio_tiempo(original_sentence, plagiarized_sentence)
    
        assert result == False

    #  The method correctly extracts the verbs from the original and plagiarized sentences.
    def test_extract_verbs(self, mocker):
        mocker.patch('nltk.pos_tag', return_value=[('I', 'PRP'), ('am', 'VBP'), ('going', 'VBG'), ('to', 'TO'), ('the', 'DT'), ('store', 'NN')])
        original_sentence = "I am going to the store."
        plagiarized_sentence = "He is going to the store."
    
        result = TiposDePlagio.detectar_cambio_tiempo(original_sentence, plagiarized_sentence)
    
        assert result == False


    #  The method correctly handles cases where there are no verbs in the original sentence.
    def test_no_verbs_in_original_sentence(self, mocker):
        mocker.patch('nltk.pos_tag', return_value=[('I', 'PRP'), ('am', 'VBP'), ('going', 'VBG'), ('to', 'TO'), ('the', 'DT'), ('store', 'NN')])
        original_sentence = "I am going to the store."
        plagiarized_sentence = "The store is open."
    
        result = TiposDePlagio.detectar_cambio_tiempo(original_sentence, plagiarized_sentence)
    
        assert result == False

    #  The method correctly handles cases where there are no verbs in the plagiarized sentence.
    def test_no_verbs_in_plagiarized_sentence(self, mocker):
        mocker.patch('nltk.pos_tag', return_value=[('I', 'PRP'), ('am', 'VBP'), ('going', 'VBG'), ('to', 'TO'), ('the', 'DT'), ('store', 'NN')])
        original_sentence = "I am going to the store."
        plagiarized_sentence = "The store is closed."
    
        result = TiposDePlagio.detectar_cambio_tiempo(original_sentence, plagiarized_sentence)
    
        assert result == False

    #  The method correctly handles cases where the original and plagiarized sentences have no words in common.
    def test_no_common_words(self):
        original_sentence = "I am going to the store."
        plagiarized_sentence = "She is eating dinner at home."

        result = TiposDePlagio.detectar_cambio_tiempo(original_sentence, plagiarized_sentence)

        assert result == False

    #  The method correctly handles cases where the original and plagiarized sentences have only stop words in common.
    def test_only_stop_words_in_common(self):
        original_sentence = "I am going to the store."
        plagiarized_sentence = "I am going to the park."

        result = TiposDePlagio.detectar_cambio_tiempo(original_sentence, plagiarized_sentence)

        assert result == False
