from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import LancasterStemmer
from sklearn.metrics.pairwise import cosine_similarity
#from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import re


#lemmatizer = WordNetLemmatizer() #lemmatizer algorithm
lancStemmer = LancasterStemmer() #stemming algorithm Lancaster

text1 = "Esta es una prueba. De los famosos n-gramas. Se esta usando NLTK. A diferencia de la detección de IA, que todavía es relativamente nueva y está evolucionando, la detección de plagio existe desde hace tiempo."
text2 = "Esta es otra prueba. Esto es para el ejercicio. Usando n-gramas en clase. A diferencia de una herramienta de IA, un periodista o redactor puede mantener conversaciones reales con expertos en la materia sobre la que escribe."


#----------- PREPROCESSING --------------
def get_stemmer(text):
  palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
  text_lista = []
  for palabra in palabras:
    nueva = lancStemmer.stem(palabra)
    text_lista.append(nueva)
  nuevo_texto = ' '.join(text_lista)
  return nuevo_texto

""" def get_lemm(text):
  palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
  text_lista = []
  for palabra in palabras:
    nueva = lemmatizer.lemmatize(palabra)
    text_lista.append(nueva)
  nuevo_texto = ' '.join(text_lista)
  return nuevo_texto """

def get_grams(text, n):
  text = get_stemmer(text) #pre-procesa el parrafo
  text = re.findall(r"\w+", text) #separa los caracteres pre-procesados del parrafo en listas
  grams = ngrams(text,n) #genera los ngrams
  result = []
  for ng in grams:
    result.append(' '.join(ng)) #agrega los ngrams en una lista llamada result
  return result

def matriz_parrafos(text1, text2, n):
  grams1 = get_grams(text1, n)
  grams2 = get_grams (text2, n)
  grams_palabras = set(grams1 + grams2) #set de palabras de ambos ngrams
  grams_juntos = [grams1, grams2] #lista con ambas listas de los ngrams de cada parrafo
  matriz = []
  for grama in grams_juntos:
    vector = []
    for palabra in grams_palabras:
      vector.append(1 if palabra in grama else 0) #compara las palabras de los grams a la palabra y agrega o un 1 o un 0 al vector del parrafo
    matriz.append(vector)
  return matriz

#print (get_lemm(text1))
# print(get_grams(text1, 2))
print(matriz_parrafos(text1, text2, 2))

similitud = cosine_similarity(matriz_parrafos(text1, text2, 1))
print(similitud)
print("\nSimilitud de Coseno entre parrafo 1 y 2:",similitud[0][1])

# ------------------- PROCESS ------------------

