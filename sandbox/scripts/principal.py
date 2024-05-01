from sklearn.metrics.pairwise import cosine_similarity
import nltk
import os
import difflib
from fpdf import FPDF

import numpy as np
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from nltk.util import ngrams
import gensim.downloader as api
import re

lancStemmer = LancasterStemmer()  # stemming algorithm Lancaster

lemmatizer = WordNetLemmatizer() #lemmatizer algorithm

word_vectors = api.load("glove-wiki-gigaword-100")

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

def get_lemmatizer(text):
    palabras = remove_stopwords(text)
    palabras = palabras.split()
    text_lista = []
    for palabra in palabras:
        nueva = lemmatizer.lemmatize(palabra)
        text_lista.append(nueva)
    nuevo_texto = ' '.join(text_lista)
    return nuevo_texto

def get_grams(text, n):
    orig_text = text
    text = get_lemmatizer(text)  # pre-procesa el parrafo
    text2 = get_stemmer(text)  # pre-procesa el parrafo

    print(f'texto original: {orig_text} \n texto lematizado: {text} \n texto stemmer: {text2} \n ---------------------- \n')
    text = text.split()  # separa los caracteres pre-procesados del parrafo en listas
    if n == 0:
        return text
    else:
        grams = ngrams(text, n)  # genera los ngrams
        result = []
        for ng in grams:
            result.append(' '.join(ng))  # agrega los ngrams en una lista llamada result
        return result


def pre_procesados(folder_path, n):
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
            vector.append(
                1 if palabra in grama else 0)  # compara las palabras de los grams a la palabra y agrega 1 o 0 al vector del parrafo
        matriz.append(vector)
    return matriz


# Obtener n-gramas preprocesados
folder_path = "../../textos_plagiados"  # Ruta de la carpeta con los textos plagiados
preprocess_plagiados = pre_procesados(folder_path, 3)

folder_path_og = "../../docs_originales"  # Ruta de la carpeta con los textos originales
preprocess_originales = pre_procesados(folder_path_og, 3)

for id_plagiado, (name_plagiado, grams_plagiado) in enumerate(preprocess_plagiados, 1):
    # print(f'\nDocumento analizado: {name_plagiado}')
    for id_original, (name_original, grams_original) in enumerate(preprocess_originales, 1):
        similitud = cosine_similarity(matriz_parrafos(grams_plagiado, grams_original))
        # print(f"Similitud de Coseno entre {name_plagiado} y {name_original}: {similitud[0][1]}")

resultados = []
for id_plagiado, (name_plagiado, grams_plagiado) in enumerate(preprocess_plagiados, 1):
    for id_original, (name_original, grams_original) in enumerate(preprocess_originales, 1):
        similitud = cosine_similarity(matriz_parrafos(grams_plagiado, grams_original))
        if similitud[0][1] != 0.0 and similitud[0][1] >= 0.2:
            resultados.append([name_plagiado, name_original, similitud[0][1]])

resultados.sort(key=lambda x: x[2], reverse=True)
lista_titulos = []
for resultado in resultados:
    for plagiados in preprocess_plagiados:
        if plagiados[0] == resultado[0]:
            lista_titulos.append([plagiados[0], resultado[1]])


def buscar_y_tokenizar(directorio, nombre_archivo):
    for filename in os.listdir(directorio):
        if filename == nombre_archivo:
            filepath = os.path.join(directorio, filename)
            with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                text = file.read()
                sentences = nltk.sent_tokenize(text)
                return sentences
    return None


def encontrar_coincidencias(sentences_originales, sentences_plagiados):
    coincidencias = []
    # Contadores para la matriz de auc
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for sentence_orig in sentences_originales:
        for sentence_plag in sentences_plagiados:
            matcher = difflib.SequenceMatcher(None, sentence_orig, sentence_plag)
            match = matcher.find_longest_match(0, len(sentence_orig), 0, len(sentence_plag))
            if match.size > 0:
                # Aplicar stemming y eliminar stopwords a las coincidencias antes de contar las palabras
                cadena_orig_stemmed = get_stemmer(sentence_orig[match.a:match.a + match.size])
                cadena_plag_stemmed = get_stemmer(sentence_plag[match.b:match.b + match.size])
                # Contar las palabras en las coincidencias después de aplicar el stemming y eliminar las stopwords
                palabras_orig = cadena_orig_stemmed.split()
                palabras_plag = cadena_plag_stemmed.split()

                if len(palabras_orig) > 3 and len(palabras_plag) > 3:  # Solo considerar coincidencias con más de una palabra
                    coincidencias.append({
                        "cadena_orig": sentence_orig[match.a:match.a + match.size],
                        "cadena_plag": sentence_plag[match.b:match.b + match.size],
                        "longitud": match.size
                    })
                    # Actualizar contadores de la matriz de auc
                    if sentence_orig == sentence_plag:
                      TP += 1
                    else:
                      FP += 1
            else:
              if sentence_orig not in sentences_originales:
                TN += 1
              else:
                FN += 1
    matriz_auc = {
        'TP': TP,
        'FP': FP,
        'TN': TN,
        'FN': FN
    }
    # print(matriz_auc)

    return coincidencias, matriz_auc

total_coincidencias = []
total_TP = 0
total_FP = 0
total_TN = 0
total_FN = 0

for titulo in resultados:
    resultados = []
    sentences_originales = buscar_y_tokenizar(folder_path_og, titulo[1])
    sentences_plagiados = buscar_y_tokenizar(folder_path, titulo[0])
    # print(f"Titulo: {titulo[0]}")

    if sentences_originales and sentences_plagiados:
        # Similitud = calcular_similitud_ngramas(sentences_originales, sentences_plagiados, 3)
        similitud = titulo[2]
        # print(f"Similitud entre '{titulo[0]}' y '{titulo[1]}': {similitud * 100:.2f}%")
        coincidencias, matriz_auc = encontrar_coincidencias(sentences_originales, sentences_plagiados)
        # Actualizar contadores totales de la matriz de auc
        total_TP += matriz_auc['TP']
        total_FP += matriz_auc['FP']
        total_TN += matriz_auc['TN']
        total_FN += matriz_auc['FN']
        # print(f"Coincidencias para '{titulo[0]}' y '{titulo[1]}':")
        total_coincidencias.extend(coincidencias)

        # print("----------------------------\n")
        for coincidencia in coincidencias:
            # print(f"Cadena original: {coincidencia['cadena_orig']} (Longitud: {coincidencia['longitud']})")
            # print(f"Cadena plagiada: {coincidencia['cadena_plag']}")
            print()
    else:
        # print(f"No se encontraron oraciones en '{titulo[0]}' o '{titulo[1]}'")
        print()
    # print("----------------------------\n")

# Calculando TPR, FPR y AUC
TPR = total_TP / (total_TP + total_FN) if (total_TP + total_FN) != 0 else 0
FPR = total_FP / (total_FP + total_TN) if (total_FP + total_TN) != 0 else 0
AUC = (1 + TPR - FPR) / 2

# Imprimiendo los valores calculados
# print(f"TPR (Tasa de Verdaderos Positivos): {TPR:.2f}")
# print(f"FPR (Tasa de Falsos Positivos): {FPR:.2f}")
# print(f"AUC (Área bajo la curva ROC): {AUC:.2f}")