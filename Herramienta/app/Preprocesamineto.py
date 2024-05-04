from typing import List, Tuple
import os
import re
import nltk
from nltk.stem import LancasterStemmer
from nltk.util import ngrams
from nltk.corpus import stopwords


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

    def get_grams(self, texto: str, ngram_number: int) -> List[str]:
        """
        Esta función recibe un texto y un número de ngramas y devuelve los ngramas
        Args: texto: str, ngram_number: int
        Returns: List[str]
        
        """
        stemmed_text = self.get_stemmer(texto)
        text = re.findall(r"\w+", stemmed_text)
        grams = ngrams(text, ngram_number)
        result = []
        for ng in grams:
            result.append(' '.join(ng))
        return result

    def pre_procesados(self, folder_path: str, n: int) -> List[Tuple[str, List[str]]]:
        """
        Esta función recibe una ruta y un número de ngramas y devuelve los textos preprocesados
        Args: folder_path: str, n: int
        Returns: List[Tuple[str, List[str]]]
        """
        preprocess_texts = []
        for fileid in os.listdir(folder_path):
            if fileid.endswith(".txt"):
                filepath = os.path.join(folder_path, fileid)
                with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                    text = file.read()
                    grams = self.get_grams(text, n)
                    preprocess_texts.append((fileid, grams))
        return preprocess_texts


