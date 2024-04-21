from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
# from sklearn.metrics.pairwise import cosine_similarity

import re


class Data:
    def __init__(self):
        self.data = []
        self.texto = ""
        self.ngram_number = 1
        self.result = []

    @staticmethod
    def get_stemmer(self, texto: str) -> str:
        lancaster = LancasterStemmer()
        palabras = [palabra.lower() for palabra in re.findall(r'\w+', texto.lower())]
        text_lista = []
        for palabra in palabras:
            nueva = lancaster.stem(palabra)
            text_lista.append(nueva)
        nuevo_texto = ' '.join(text_lista)
        return nuevo_texto

    # def get_lemmatizer(self, texto: str):
    #     wordnet_lemmatizer = WordNetLemmatizer()
    #     palabras = [palabra.lower() for palabra in re.findall(r'\w+', texto.lower())]
    #     text_lista = []
    #     for palabra in palabras:
    #         nueva = wordnet_lemmatizer.lemmatize(palabra)
    #         text_lista.append(nueva)
    #     nuevo_texto = ' '.join(text_lista)
    #     return nuevo_texto

    # def get_stopwords(self):
    #     stop_words = set(stopwords.words('english'))
    #     palabras = [palabra.lower() for palabra in re.findall(r'\w+', self.lower())]
    #     text_lista = []
    #     for palabra in palabras:
    #         if palabra not in stop_words:
    #             text_lista.append(palabra)
    #     nuevo_texto = ' '.join(text_lista)
    #     return nuevo_texto

    def get_grams(self, texto: str, ngram_number: int) -> list:
        stemmed_text = self.get_stemmer(self, texto)  # aplica el stemming al texto
        # TODO: Habilitar la opcion de preprocesamiento deseada (lematizacion o stemming)
        # lemmantized_text = self.get_lemmatizer(self, texto)  # aplica la lematizacion al texto
        # TODO: Hablitar la opcion de eliminar las stop words o no
        # with_stop_words_text = self.get_stopwords(self, texto)  # elimina las stop words del texto
        text = re.findall(r"\w+", stemmed_text)  # separa los caracteres pre-procesados del parrafo en listas
        grams = ngrams(text, ngram_number)  # genera los ngrams
        result = []
        for ng in grams:
            result.append(' '.join(ng))  # agrega los ngrams en una lista llamada result
        return result