import os
import difflib
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import re
import numpy as np
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams


# Descargar recursos de NLTK
nltk.download('stopwords')
lancStemmer = LancasterStemmer()

def remove_stopwords(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
    text_lista = [palabra for palabra in palabras if palabra not in stopwords]
    return ' '.join(text_lista)

def get_stemmer(text):
    palabras = remove_stopwords(text).split()
    return ' '.join(lancStemmer.stem(palabra) for palabra in palabras)

def get_grams(text, n):
    text = get_stemmer(text)
    text = text.split()
    return text if n == 0 else [' '.join(ng) for ng in ngrams(text, n)]

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
    grams_palabras = set(grams1 + grams2)
    matriz = []
    for grama in [grams1, grams2]:
        vector = [1 if palabra in grama else 0 for palabra in grams_palabras]
        matriz.append(vector)
    return matriz

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
    for sentence_orig in sentences_originales:
        for sentence_plag in sentences_plagiados:
            matcher = difflib.SequenceMatcher(None, sentence_orig, sentence_plag)
            match = matcher.find_longest_match(0, len(sentence_orig), 0, len(sentence_plag))
            if match.size > 0:
                cadena_orig_stemmed = get_stemmer(sentence_orig[match.a:match.a + match.size])
                cadena_plag_stemmed = get_stemmer(sentence_plag[match.b:match.b + match.size])
                palabras_orig = remove_stopwords(cadena_orig_stemmed).split()
                palabras_plag = remove_stopwords(cadena_plag_stemmed).split()
                if len(palabras_orig) > 1 and len(palabras_plag) > 1:
                    coincidencias.append({
                        "cadena_orig": sentence_orig[match.a:match.a + match.size],
                        "cadena_plag": sentence_plag[match.b:match.b + match.size],
                        "longitud": match.size
                    })
    return coincidencias

def calcular_similitud_ngramas(sentences_originales, sentences_plagiados, n):
    grams_originales = [gram for sentence in sentences_originales for gram in get_grams(sentence, n)]
    grams_plagiados = [gram for sentence in sentences_plagiados for gram in get_grams(sentence, n)]
    matriz = matriz_parrafos(grams_originales, grams_plagiados)
    return cosine_similarity(matriz)[0][1]

def crear_documento_pdf(titulo, similitud, coincidencias):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Resultados de prueba de plagio: {titulo[1]}", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Plagio detectado: {similitud * 100:.2f}%", ln=True, align="C")
    pdf.ln(5)
    for coincidencia in coincidencias:
        cadena_orig = coincidencia['cadena_orig']
        cadena_plag = coincidencia['cadena_plag']
        texto = f"Texto original: {cadena_orig}\nTexto plagiado: {cadena_plag}\n\n"
        pdf.set_font("Arial", style="B")
        pdf.multi_cell(0, 10, txt=texto, border=1, align="L")
    nombre_archivo = f"Resultado_similitud_{titulo[0]}_y_{titulo[1]}.pdf"
    ruta_archivo = os.path.join("/app/Resultados", nombre_archivo)
    pdf.output(ruta_archivo)

def main():
    folder_path = "/textos_plagiados"
    folder_path_og = "/docs_originales"
    preprocess_plagiados = pre_procesados(folder_path, 3)
    preprocess_originales = pre_procesados(folder_path_og, 3)
    lista_titulos = []
    for id_plagiado, (name_plagiado, grams_plagiado) in enumerate(preprocess_plagiados, 1):
        for id_original, (name_original, grams_original) in enumerate(preprocess_originales, 1):
            similitud = calcular_similitud_ngramas(buscar_y_tokenizar(folder_path_og, name_original),
                                                   buscar_y_tokenizar(folder_path, name_plagiado),
                                                   0)
            if similitud != 0.0 and similitud >= 0.2:
                lista_titulos.append([name_plagiado, name_original])
    for titulo in lista_titulos:
        sentences_originales = buscar_y_tokenizar(folder_path_og, titulo[1])
        sentences_plagiados = buscar_y_tokenizar(folder_path, titulo[0])
        if sentences_originales and sentences_plagiados:
            similitud = calcular_similitud_ngramas(sentences_originales, sentences_plagiados, 0)
            coincidencias = encontrar_coincidencias(sentences_originales, sentences_plagiados)
            crear_documento_pdf(titulo, similitud, coincidencias)

if __name__ == "__main__":
    main()
