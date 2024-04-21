from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('stopwords')
import numpy as np
from nltk.stem import LancasterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
#from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import re
import os

lancStemmer = LancasterStemmer() #stemming algorithm Lancaster
#lemmatizer = WordNetLemmatizer() #lemmatizer algorithm

def remove_stopwords(text):
  stopwords = set(nltk.corpus.stopwords.words('english'))
  palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
  text_lista = []
  for palabra in palabras:
    if palabra not in stopwords:
      text_lista.append(palabra)
  nuevo_texto = ' '.join(text_lista)
  return nuevo_texto

def get_stemmer(text):
  palabras = remove_stopwords(text)
  palabras = palabras.split()
  text_lista = []
  for palabra in palabras:
    nueva = lancStemmer.stem(palabra)
    text_lista.append(nueva)
  nuevo_texto = ' '.join(text_lista)
  return nuevo_texto

def get_grams(text, n):
  text = get_stemmer(text) #pre-procesa el parrafo
  text = text.split() #separa los caracteres pre-procesados del parrafo en listas
  grams = ngrams(text,n) #genera los ngrams
  result = []
  for ng in grams:
    result.append(' '.join(ng)) #agrega los ngrams en una lista llamada result
  return result

def pre_procesados (folder_path, n):
  preprocess_texts = []
  for fileid in os.listdir(folder_path):
    if fileid.endswith(".txt"):
      filepath = os.path.join(folder_path, fileid)
      with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
        text = file.read()
        grams = get_grams(text, n)
        preprocess_texts.append((fileid, grams))
  return preprocess_texts

def matriz_parrafos(grams1, grams2):
    grams_palabras = set(grams1 + grams2)  # set de palabras de ambos ngrams
    grams_juntos = [grams1, grams2]  # lista con ambas listas de los ngrams de cada parrafo
    matriz = []
    for grama in grams_juntos:
        vector = []
        for palabra in grams_palabras:
            vector.append(1 if palabra in grama else 0)  # compara las palabras de los grams a la palabra y agrega 1 o 0 al vector del parrafo
        matriz.append(vector)
    return matriz

# Obtener n-gramas preprocesados
folder_path = "../DetectorPlagio/textos_plagiados"
preprocess_plagiados = pre_procesados(folder_path, 2)

folder_path_og = "../DetectorPlagio/docs_org"
preprocess_originales = pre_procesados(folder_path_og, 2)

for id_plagiado, (name_plagiado, grams_plagiado) in enumerate(preprocess_plagiados, 1):
    print(f'\nDocumento analizado: {name_plagiado}')
    for id_original, (name_original, grams_original) in enumerate(preprocess_originales, 1):
        similitud = cosine_similarity(matriz_parrafos(grams_plagiado, grams_original))
        print(f"Similitud de Coseno entre {name_plagiado} y {name_original}: {similitud[0][1]}")
