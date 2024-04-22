from sklearn.metrics.pairwise import cosine_similarity
import nltk
import os
import difflib
from fpdf import FPDF
nltk.download('stopwords')
import numpy as np
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import re


lancStemmer = LancasterStemmer()  # stemming algorithm Lancaster

# lemmatizer = WordNetLemmatizer() #lemmatizer algorithm
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
    text = get_stemmer(text)  # pre-procesa el parrafo
    text = text.split()  # separa los caracteres pre-procesados del parrafo en listas
    if n == 0:
        return text
    else:
        grams = ngrams(text, n)  # genera los ngrams
        result = []
        for ng in grams:
            result.append(' '.join(ng))  # agrega los ngrams en una lista llamada result
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
            vector.append(
                1 if palabra in grama else 0)  # compara las palabras de los grams a la palabra y agrega 1 o 0 al vector del parrafo
        matriz.append(vector)
    return matriz

# Obtener n-gramas preprocesados
folder_path = "/Users/sergiogonzalez/Documents/GitHub/DetectorPlagio/textos_plagiados" # Ruta de la carpeta con los textos plagiados
preprocess_plagiados = pre_procesados(folder_path, 3)

folder_path_og = "/Users/sergiogonzalez/Documents/GitHub/DetectorPlagio/docs_originales" # Ruta de la carpeta con los textos originales
preprocess_originales = pre_procesados(folder_path_og, 3)

for id_plagiado, (name_plagiado, grams_plagiado) in enumerate(preprocess_plagiados, 1):
    print(f'\nDocumento analizado: {name_plagiado}')
    for id_original, (name_original, grams_original) in enumerate(preprocess_originales, 1):
        similitud = cosine_similarity(matriz_parrafos(grams_plagiado, grams_original))
        print(f"Similitud de Coseno entre {name_plagiado} y {name_original}: {similitud[0][1]}")
        
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

    for sentence_orig in sentences_originales:
        for sentence_plag in sentences_plagiados:
            matcher = difflib.SequenceMatcher(None, sentence_orig, sentence_plag)
            match = matcher.find_longest_match(0, len(sentence_orig), 0, len(sentence_plag))
            if match.size > 0:
                # Aplicar stemming y eliminar stopwords a las coincidencias antes de contar las palabras
                cadena_orig_stemmed = get_stemmer(sentence_orig[match.a:match.a + match.size])
                cadena_plag_stemmed = get_stemmer(sentence_plag[match.b:match.b + match.size])
                # Contar las palabras en las coincidencias después de aplicar el stemming y eliminar las stopwords
                palabras_orig = remove_stopwords(cadena_orig_stemmed).split()
                palabras_plag = remove_stopwords(cadena_plag_stemmed).split()
                if len(palabras_orig) > 1 and len(palabras_plag) > 1:  # Solo considerar coincidencias con más de una palabra
                    coincidencias.append({
                        "cadena_orig": sentence_orig[match.a:match.a + match.size],
                        "cadena_plag": sentence_plag[match.b:match.b + match.size],
                        "longitud": match.size
                    })

    return coincidencias

def calcular_similitud_ngramas(sentences_originales, sentences_plagiados, n):
    grams_originales = []
    grams_plagiados = []

    for sentence in sentences_originales:
        grams_originales.extend(get_grams(sentence, n))
    for sentence in sentences_plagiados:
        grams_plagiados.extend(get_grams(sentence, n))
        

    matriz = matriz_parrafos(grams_originales, grams_plagiados)
    # Calcular la similitud coseno entre las matrices de n-gramas
    similitud = cosine_similarity(matriz)[0][1]

    return similitud

for titulo in lista_titulos:
    resultados = []
    sentences_originales = buscar_y_tokenizar(folder_path_og, titulo[1])
    sentences_plagiados = buscar_y_tokenizar(folder_path, titulo[0])
    print(f"Titulo: {titulo[0]}")
    
    if sentences_originales and sentences_plagiados:
        similitud = calcular_similitud_ngramas(sentences_originales, sentences_plagiados, 0) 
        print(f"Similitud entre '{titulo[0]}' y '{titulo[1]}': {similitud * 100:.2f}%")
        coincidencias = encontrar_coincidencias(sentences_originales, sentences_plagiados)
        print(f"Coincidencias para '{titulo[0]}' y '{titulo[1]}':")
        
        for coincidencia in coincidencias:
            print(f"Cadena original: {coincidencia['cadena_orig']} (Longitud: {coincidencia['longitud']})")
            print(f"Cadena plagiada: {coincidencia['cadena_plag']}")
            print()
    else:
        print(f"No se encontraron oraciones en '{titulo[0]}' o '{titulo[1]}'")
    print("----------------------------\n")

def crear_documento_pdf(titulo, similitud, coincidencias):
    # Crear un nuevo objeto PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Agregar una página
    pdf.add_page()

    # Establecer la fuente y el tamaño del texto
    pdf.set_font("Arial", size=12)

    # Título del documento
    pdf.cell(200, 10, txt=f"Resultados de prueba de plagio: {titulo[1]}", ln=True, align="C")

    # Plagio detectado
    pdf.cell(200, 10, txt=f"Plagio detectado: {similitud * 100:.2f}%", ln=True, align="C")
    pdf.ln(5)

    # Texto con resaltado de las coincidencias
    for coincidencia in coincidencias:
        cadena_orig = coincidencia['cadena_orig']
        cadena_plag = coincidencia['cadena_plag']
        # Verificar si existe la clave 'referencia'
        if 'referencia' in coincidencia:
            referencia = coincidencia['referencia']
            texto = f"Texto original: {cadena_orig}\nTexto plagiado: {cadena_plag}\nReferencia: {referencia}\n\n"
        else:
            texto = f"Texto original: {cadena_orig}\nTexto plagiado: {cadena_plag}\n\n"
        pdf.set_font("Arial", style="B")
        pdf.multi_cell(0, 10, txt=texto, border=1, align="L")

    # Guardar el documento PDF en la carpeta de resultados
    nombre_archivo = f"Resultado_similitud_{titulo[0]}_y_{titulo[1]}.pdf"
    ruta_archivo = os.path.join("/Users/sergiogonzalez/Documents/GitHub/DetectorPlagio/app/Resultados", nombre_archivo)
    pdf.output(ruta_archivo)


for titulo in lista_titulos:
    resultados = []
    sentences_originales = buscar_y_tokenizar(folder_path_og, titulo[1])
    sentences_plagiados = buscar_y_tokenizar(folder_path, titulo[0])

    if sentences_originales and sentences_plagiados:
        similitud = calcular_similitud_ngramas(sentences_originales, sentences_plagiados, 0) 
        coincidencias = encontrar_coincidencias(sentences_originales, sentences_plagiados)
            
        # Llamar a la función para crear el documento PDF
        crear_documento_pdf(titulo, similitud, coincidencias)