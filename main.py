from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import LancasterStemmer
from nltk.util import ngrams
import re
import os
lancStemmer = LancasterStemmer() #stemming algorithm Lancaster

text1 = "Esta es una prueba. De los famosos n-gramas. Se esta usando NLTK. A diferencia de la detección de IA, que todavía es relativamente nueva y está evolucionando, la detección de plagio existe desde hace tiempo."
text2 = "Esta es otra prueba. Esto es para el ejercicio. Usando n-gramas en clase. A diferencia de una herramienta de IA, un periodista o redactor puede mantener conversaciones reales con expertos en la materia sobre la que escribe."



def get_stemmer(text):
  palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
  text_lista = []
  for palabra in palabras:
    nueva = lancStemmer.stem(palabra)
    text_lista.append(nueva)
  nuevo_texto = ' '.join(text_lista)
  return nuevo_texto




def get_grams(text, n):
  text = get_stemmer(text) #pre-procesa el parrafo
  text = re.findall(r"\w+", text) #separa los caracteres pre-procesados del parrafo en listas
  grams = ngrams(text,n) #genera los ngrams
  result = []
  for ng in grams:
    result.append(' '.join(ng)) #agrega los ngrams en una lista llamada result
  return result

def matriz_parrafos(gramas1, gramas2):
  grams_palabras = set(gramas1 + gramas2) #set de palabras de ambos ngrams
  grams_juntos = [gramas1, gramas2] #lista con ambas listas de los ngrams de cada parrafo
  matriz = []
  for grama in grams_juntos:
    vector = []
    for palabra in grams_palabras:
      vector.append(1 if palabra in grama else 0) #compara las palabras de los grams a la palabra y agrega o un 1 o un 0 al vector del parrafo
    matriz.append(vector)
  return matriz

def cargar_docs(ruta):
  with open(ruta, 'r') as file:
    return file.read()

def similitud_documento(doc1, doc2):
    unigrams_doc1 = get_grams(doc1, 1)
    bigrams_doc1 = get_grams(doc1, 2)
    trigrams_doc1 = get_grams(doc1, 3)

    unigrams_doc2 = get_grams(doc2, 1)
    bigrams_doc2 = get_grams(doc2, 2)
    trigrams_doc2 = get_grams(doc2, 3)

    similitud_unigrams = cosine_similarity(matriz_parrafos(unigrams_doc1, unigrams_doc2))
    similitud_bigrams = cosine_similarity(matriz_parrafos(bigrams_doc1, bigrams_doc2))
    similitud_trigrams = cosine_similarity(matriz_parrafos(trigrams_doc1, trigrams_doc2))

    print("Similitud de coseno (unigrams) entre doc1 y doc2:", similitud_unigrams[0][1])
    print("Similitud de coseno (bigrams) entre doc1 y doc2:", similitud_bigrams[0][1])
    print("Similitud de coseno (trigrams) entre doc1 y doc2:", similitud_trigrams[0][1])

ruta_dataset = "dataset.txt"
doc1 = cargar_docs(os.path.join(ruta_dataset, "documento_org1.txt"))
doc2 = cargar_docs(os.path.join(ruta_dataset, "documento_org2.txt"))

similitud_documento(doc1, doc2)