from typing import List, Tuple, LiteralString
import os
import re
import nltk
from gensim.models.doc2vec import TaggedDocument
from nltk.stem import LancasterStemmer
from nltk.util import ngrams
from nltk.corpus import stopwords

nltk.download('wordnet')
from gensim.models import Word2Vec
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('wordnet')
from nltk.util import ngrams

import re

nltk.download('averaged_perceptron_tagger')
lemmatizer = WordNetLemmatizer()  #lemmatizer algorithm
lancStemmer = LancasterStemmer()  # stemming algorithm Lancaster


class Preprocesamiento:
    def __init__(self) -> None:
        self.data: List[Tuple[str, List[str]]] = []
        self.texto: str = ""
        self.ngram_number: int = 1
        self.result: List[List[int]] = []
        self.lancStemmer = LancasterStemmer()

    @staticmethod
    def remove_stopwords(text: str) -> str:
        """
        Esta función recibe un texto y elimina las stopwords
        Args: text: str
        Returns: str
        """
        stopwords = set(nltk.corpus.stopwords.words('english'))
        palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
        text_lista = []
        for palabra in palabras:
            if palabra not in stopwords:
                text_lista.append(palabra)
        nuevo_texto = ' '.join(text_lista)
        return nuevo_texto

    def get_lemmatizer(self, text: str) -> str:
        palabras = self.remove_stopwords(text)
        palabras = palabras.split()
        text_lista = []
        for palabra in palabras:
            nueva = lemmatizer.lemmatize(palabra)
            text_lista.append(nueva)
        nuevo_texto = ' '.join(text_lista)
        return nuevo_texto

    def get_stemmer(self, texto: str) -> str:
        """
        Esta función recibe un texto y lo devuelve tokenizado y con stemming
        Args: texto: str
        Returns: str
        """
        palabras = self.remove_stopwords(texto)
        palabras = palabras.split()
        text_lista = []
        for palabra in palabras:
            nueva = self.lancStemmer.stem(palabra)
            text_lista.append(nueva)
        nuevo_texto = ' '.join(text_lista)
        return nuevo_texto

    @staticmethod
    def buscar_y_tokenizar(directorio: str, nombre_archivo: str) -> List[str]:
        """
        Esta función recibe un directorio y un nombre de archivo y devuelve las oraciones tokenizadas
        Args: directorio: str, nombre_archivo: str
        Returns: List[str]
        """
        for filename in os.listdir(directorio):
            if filename == nombre_archivo:
                filepath = os.path.join(directorio, filename)
                with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                    text = file.read()
                    sentences = nltk.sent_tokenize(text)
                    return sentences
        return []

    def get_grams(self, text: str, ngram: int, method: str) -> LiteralString | str | list[LiteralString | str]:
        result = []

        if method == 'lemmatize':
            text = self.get_lemmatizer(text)
            if ngram == 0:  # Si ngram es 0, se retorna el texto completo sin ngramas
                text = nltk.sent_tokenize(text)
                text = ' '.join(text)
                return text

            else:
                text = text.split()
                grams = ngrams(text, ngram)
                for ng in grams:
                    result.append(' '.join(ng))
        elif method == 'stemmer':
            text = self.get_stemmer(text)
            if ngram == 0:  # Si ngram es 0, se retorna el texto completo sin ngramas
                text = nltk.sent_tokenize(text)
                text = ' '.join(text)
                return text

            else:
                text = text.split()
                grams = ngrams(text, ngram)
                for ng in grams:
                    result.append(' '.join(ng))
        else:
            raise ValueError('Method not found')

        return result

    def preprocess_docs(self, folder_path: str, ngram: int, method: str) -> list[str] | LiteralString | str | list[
        LiteralString | str]:
        """
        Esta función recibe la ruta de una carpeta con documentos de texto
        y retorna una lista de documentos preprocesados y taggeados para el modelo
        """
        tagged_documents = []
        lemmatizer = WordNetLemmatizer()

        for fileid in os.listdir(folder_path):
            if fileid.endswith(".txt"):
                filepath = os.path.join(folder_path, fileid)

                with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                    text = file.read()
                    # Preprocesamiento de texto
                    grams = self.get_grams(text, ngram, method)
                    # Ensure words are split into a list of strings and then converted to tuple
                    words = tuple(word.split() for word in grams)
                    # Flatten the list of lists into a single list of strings
                    words = [word for sublist in words for word in sublist if word.isalpha()]
                    tagged_documents.append(TaggedDocument(words=words, tags=[fileid]))

        return tagged_documents

    def preprocess_sentences(self, sentences: List[str]) -> List[TaggedDocument]:
        """
        Función para preprocesar las oraciones.
        Después de tokenizar las oraciones:
        Se eliminan las stopwords y se lematizan las palabras.
        Se tagean las oraciones con un identificador único.
        """
        tagged_sentences = []
        lemmatizer = WordNetLemmatizer()
        for i, sentence in enumerate(sentences):
            tagged_sentence = TaggedDocument(
                words=[lemmatizer.lemmatize(word) for word in nltk.word_tokenize(sentence.lower()) if word.isalpha()],
                tags=[str(i)])
            tagged_sentences.append(tagged_sentence)
        return tagged_sentences

    def buscar_y_tokenizar(self, directorio, nombre_archivo):
        """
        Esta función recibe la ruta de un directorio y el nombre de un archivo
        y retorna una lista de oraciones tokenizadas del archivo
        ejemplo de salida: ['Primera oración.', 'Segunda oración.']
        """
        for filename in os.listdir(directorio):
            if filename == nombre_archivo:
                filepath = os.path.join(directorio, filename)
                with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                    text = file.read()
                    sentences = nltk.sent_tokenize(text)
                    return sentences
        return None