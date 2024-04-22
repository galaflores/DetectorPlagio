# import difflib
# from typing import List, Dict, Any, Tuple
# from app.Preprocesamineto import Preprocesamiento
# import os
# from fpdf import FPDF
#
#
# class Procesamiento:
#     @staticmethod
#     def matriz_parrafos(grams1: list, grams2: list) -> list:
#         grams_palabras = set(grams1 + grams2)  # set de palabras de ambos ngrams
#         grams_juntos = [grams1, grams2]  # lista con ambas listas de los ngrams de cada parrafo
#         matriz = []
#         for grama in grams_juntos:
#             vector = []
#             for palabra in grams_palabras:
#                 vector.append(
#                     1 if palabra in grama else 0)  # compara las palabras de los grams a la palabra y agrega 1 o 0 al vector del parrafo
#             matriz.append(vector)
#         return matriz
#
#     @staticmethod
#     def encontrar_coincidencias(sentences_originales: List[str], sentences_plagiados: List[str]) -> List[
#         Dict[str, Any]]:
#         coincidencias: List[Dict[str, Any]] = []
#         for sentence_orig in sentences_originales:
#             for sentence_plag in sentences_plagiados:
#                 matcher = difflib.SequenceMatcher(None, sentence_orig, sentence_plag)
#                 match = matcher.find_longest_match(0, len(sentence_orig), 0, len(sentence_plag))
#                 if match.size > 3:
#                     # Aplicar stemming y eliminar stopwords a las coincidencias antes de contar las palabras
#
#                     cadena_orig_stemmed = Preprocesamiento.get_stemmer(sentence_orig[match.a:match.a + match.size])
#                     cadena_plag_stemmed = Preprocesamiento.get_stemmer(sentence_plag[match.b:match.b + match.size])
#                     # Contar las palabras en las coincidencias después de aplicar el stemming y eliminar las stopwords
#                     palabras_orig = cadena_orig_stemmed.split()
#                     palabras_plag = cadena_plag_stemmed.split()
#
#                     if len(palabras_orig) > 3 and len(
#                             palabras_plag) > 3:  # Solo considerar coincidencias con más de una palabra
#                         coincidencias.append({
#                             "cadena_orig": sentence_orig[match.a:match.a + match.size],
#                             "cadena_plag": sentence_plag[match.b:match.b + match.size],
#                             "longitud": match.size
#                         })
#
#         return coincidencias
#
#     @staticmethod
#     def crear_documento_pdf(titulo: Tuple[str, str], similitud: float, coincidencias: List[Dict[str, Any]]) -> None:
#         # Crear un nuevo objeto PDF
#         pdf = FPDF()
#         pdf.set_auto_page_break(auto=True, margin=15)
#
#         # Agregar una página
#         pdf.add_page()
#
#         # Establecer la fuente y el tamaño del texto
#         pdf.set_font("Arial", size=12)
#
#         # Título del documento
#         pdf.cell(200, 10, txt=f"Resultados de prueba de plagio: {titulo[1]}", ln=True, align="C")
#
#         # Plagio detectado
#         pdf.cell(200, 10, txt=f"Plagio detectado: {similitud * 100:.2f}%", ln=True, align="C")
#         pdf.ln(5)
#
#         # Texto con resaltado de las coincidencias
#         for coincidencia in coincidencias:
#             cadena_orig = coincidencia['cadena_orig']
#             cadena_plag = coincidencia['cadena_plag']
#             # Verificar si existe la clave 'referencia'
#             if 'referencia' in coincidencia:
#                 referencia = coincidencia['referencia']
#                 texto = f"Texto original: {cadena_orig}\nTexto plagiado: {cadena_plag}\nReferencia: {referencia}\n\n"
#             else:
#                 texto = f"Texto original: {cadena_orig}\nTexto plagiado: {cadena_plag}\n\n"
#             pdf.set_font("Arial", style="B")
#             pdf.multi_cell(0, 10, txt=texto, border=1, align="L")
#
#         # Guardar el documento PDF en la carpeta de resultados
#         nombre_archivo = f"Resultado_similitud_{titulo[0]}_y_{titulo[1]}.pdf"
#         ruta_archivo = os.path.join("/Users/sergiogonzalez/Documents/GitHub/DetectorPlagio/app/Resultados",
#                                     nombre_archivo)
#         pdf.output(ruta_archivo)


import difflib
from typing import List, Dict, Any, Tuple
from app.Preprocesamineto import Preprocesamiento
import os
from fpdf import FPDF


class Procesamiento:
    @staticmethod
    def matriz_parrafos(grams1: list, grams2: list) -> list:
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

    @staticmethod
    def encontrar_coincidencias(sentences_originales: List[str], sentences_plagiados: List[str]) -> List[
        Dict[str, Any]]:
        coincidencias: List[Dict[str, Any]] = []
        for sentence_orig in sentences_originales:
            for sentence_plag in sentences_plagiados:
                matcher = difflib.SequenceMatcher(None, sentence_orig, sentence_plag)
                match = matcher.find_longest_match(0, len(sentence_orig), 0, len(sentence_plag))
                if match.size > 3:
                    # Crear instancias de la clase Preprocesamiento
                    preprocesamiento = Preprocesamiento()
                    # Llamar al método get_stemmer de Preprocesamiento
                    cadena_orig_stemmed = preprocesamiento.get_stemmer(sentence_orig[match.a:match.a + match.size])
                    cadena_plag_stemmed = preprocesamiento.get_stemmer(sentence_plag[match.b:match.b + match.size])
                    # Contar las palabras en las coincidencias después de aplicar el stemming y eliminar las stopwords
                    palabras_orig = cadena_orig_stemmed.split()
                    palabras_plag = cadena_plag_stemmed.split()

                    if len(palabras_orig) > 3 and len(
                            palabras_plag) > 3:  # Solo considerar coincidencias con más de una palabra
                        coincidencias.append({
                            "cadena_orig": sentence_orig[match.a:match.a + match.size],
                            "cadena_plag": sentence_plag[match.b:match.b + match.size],
                            "longitud": match.size
                        })

        return coincidencias

    @staticmethod
    def crear_documento_pdf(titulo: Tuple[str, str], similitud: float, coincidencias: List[Dict[str, Any]]) -> None:
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
        ruta_archivo = os.path.join("/Users/sergiogonzalez/Documents/GitHub/DetectorPlagio/app/Resultados",
                                    nombre_archivo)
        pdf.output(ruta_archivo)