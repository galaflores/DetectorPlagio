from TiposDePlagio import TiposDePlagio

import pytest

class TestDetectorCambioVoz:

    #  The method correctly identifies when there is no change of voice between the original and plagiarized sentences.
    def test_no_change_of_voice(self):
        original_sentence = "The cat is sleeping."
        plagiarized_sentence = "The cat is sleeping."
        assert TiposDePlagio.detector_cambio_voz(original_sentence, plagiarized_sentence) == False

    #  The method correctly identifies when there is a change of voice between the original and plagiarized sentences.
    def test_change_of_voice(self):
        original_sentence = "The cat is sleeping."
        plagiarized_sentence = "The cat is being fed."
        assert TiposDePlagio.detector_cambio_voz(original_sentence, plagiarized_sentence) == True

    #  The method correctly identifies when the subject of the original sentence is not a verb.
    def test_subject_not_verb_original(self):
        original_sentence = "The cat is sleeping."
        plagiarized_sentence = "The dog is sleeping."
        assert TiposDePlagio.detector_cambio_voz(original_sentence, plagiarized_sentence) == False

    #  The method correctly identifies when the original and plagiarized sentences have different verbs but the same subject.
    def test_different_verbs_same_subject(self):
        original_sentence = "The cat is sleeping."
        plagiarized_sentence = "The cat is eating."
        assert TiposDePlagio.detector_cambio_voz(original_sentence, plagiarized_sentence) == True

    #  The original sentence is empty.
    def test_empty_original_sentence(self):
        original_sentence = ""
        plagiarized_sentence = "The cat is sleeping."
        assert TiposDePlagio.detector_cambio_voz(original_sentence, plagiarized_sentence) == False

    #  The plagiarized sentence is empty.
    def test_empty_plagiarized_sentence(self):
        original_sentence = "The cat is sleeping."
        plagiarized_sentence = ""
        assert TiposDePlagio.detector_cambio_voz(original_sentence, plagiarized_sentence) == False

    #  The original and plagiarized sentences are empty.
    def test_empty_sentences(self):
        original_sentence = ""
        plagiarized_sentence = ""
        assert TiposDePlagio.detector_cambio_voz(original_sentence, plagiarized_sentence) == False

    #  The original sentence has no verbs.
    def test_no_verbs_original(self):
        original_sentence = "The cat is sleeping."
        plagiarized_sentence = "The cat sleeps."
        assert TiposDePlagio.detector_cambio_voz(original_sentence, plagiarized_sentence) == False
