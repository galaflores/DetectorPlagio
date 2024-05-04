from typing import List, Any, Literal, Tuple

import Preprocesamineto
import Procesamiento
from sklearn.metrics.pairwise import cosine_similarity


class DetectorDePlagio(Preprocesamineto.Preprocesamiento, Procesamiento.Procesamiento):
    def __init__(self):
        super().__init__()
        self.texto_stems: List[str] = []
        self.archivo_texto_stems: List[str] = []
        self.folder_path_plagiados: str = ""
        self.folder_path_originales: str = ""

    def activa_preprocesamiento(self, folder_path_plagiados: str, folder_path_originales: str, ngramas: int,
                                metodo_preprocesamiento: str) -> Tuple[
        List[str] | Literal["Error"], List[str] | Literal["Error"]]:
        """
        Esta función recibe una ruta y manda a preprocesar los textos
        Args: folder_path_plagiados: str, folder_path_originales: str, ngramas: int, metodo_preprocesamiento: str
        Returns: Tuple[List[str] | Literal["Error"], List[str] | Literal["Error"]]
        """
        tagged_originals = self.preprocess_docs(folder_path_originales, 1, metodo_preprocesamiento)
        tagged_plagiarized = self.preprocess_docs(folder_path_plagiados, 1, metodo_preprocesamiento)
        return tagged_originals, tagged_plagiarized

    def analizar_similitud(self, folder_path_plagiados: str, folder_path_originales: str,
                           metodo_preprocesamiento: str) -> List[List[Any]]:
        """
        Esta funcion recibe dos rutas y manda a preprocesar los textos y analizar la similitud
        Args: folder_path_plagiados: str, folder_path_originales: str, metodo_preprocesamiento: str
        Returns: List[List[Any]]
        """
        self.folder_path_plagiados = folder_path_plagiados
        self.folder_path_originales = folder_path_originales

        preprocess_originales, preprocess_plagiados = self.activa_preprocesamiento(folder_path_plagiados,
                                                                                   folder_path_originales, 1,
                                                                                   metodo_preprocesamiento)

        similarity_results = []
        model = self.train_doc2vec(preprocess_originales + preprocess_plagiados)

        # Iterating over each plagiarized text
        for plagio_doc in preprocess_plagiados:
            max_similarity = 0
            most_similar = ''
            most_similar_doc = ''

            # Comparing with each original document
            for original_doc in preprocess_originales:
                similarity = self.calculate_similarity_doc2vec(plagio_doc, original_doc, model)
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar = original_doc.tags[0]
                    most_similar_doc = original_doc.words

            similarity_results.append([plagio_doc.tags[0], most_similar, max_similarity, most_similar_doc])

        # Sorting results by similarity in descending order
        similarity_results.sort(key=lambda x: x[2], reverse=True)
        return similarity_results

    def encontrar_tipos_de_plagio(self, similarity_results: List[List[Any]], folder_path_plagiados: str,
                                  folder_path_originales: str) -> tuple[list[list[Any]], list[float | int]]:
        """
        Ejecución del detector de plagio con el modelo Doc2Vec entrenado y las funciones de tipo de detección de plagio.
        Se calculan las métricas de TPR, FPR y AUC.
        """
        total_coincidencias: List[Any] = []
        total_TP: int = 0
        total_FP: int = 0
        total_TN: int = 0
        total_FN: int = 0
        results: List[List[Any]] = []

        for titulo in similarity_results:
            resultados = []
            sentences_originales = self.buscar_y_tokenizar(folder_path_originales, titulo[1])
            sentences_plagiados = self.buscar_y_tokenizar(folder_path_plagiados, titulo[0])

            # print(f"Titulo: {titulo[0]}")

            if sentences_originales and sentences_plagiados:
                tagged_sentences_originales = self.preprocess_sentences(sentences_originales)
                tagged_sentences_plagiados = self.preprocess_sentences(sentences_plagiados)
                model = self.train_doc2vec(tagged_sentences_originales + tagged_sentences_plagiados)
                similitud = titulo[2]
                # print(f"Similitud entre '{titulo[0]}' y '{titulo[1]}': {similitud * 100:.2f}%")
                coincidencias, matriz_auc, tipo_plagio = self.encontrar_coincidencias(tagged_sentences_originales,
                                                                                      tagged_sentences_plagiados, model)
                total_TP += matriz_auc['TP']
                total_FP += matriz_auc['FP']
                total_TN += matriz_auc['TN']
                total_FN += matriz_auc['FN']
                # print(f"Tipo de plagio: {tipo_plagio}")
                total_coincidencias.extend(coincidencias)

                # Llamar al método para crear el documento PDF
                # self.crear_documento_pdf(titulo, similitud, coincidencias)

                # Agregar los resultados para este título
                results.append([titulo[0], titulo[1], similitud, tipo_plagio])

        # Calculando TPR, FPR y AUC
        TPR = total_TP / (total_TP + total_FN) if (total_TP + total_FN) != 0 else 0
        FPR = total_FP / (total_FP + total_TN) if (total_FP + total_TN) != 0 else 0
        AUC = (1 + TPR - FPR) / 2

        return results, [TPR, FPR, AUC]


    def imprimir_resultados(self, resultados: List[List[Any]]) -> str:
        output = ""
        output += "{:<50} | {:<10} | {:<50} | {:<7} | {:<20}\n".format(
            "Documento sospechoso (plagiado)", "Copia", "Documento plagiado (original)", "% plagio", "Tipo de plagio")
        output += "-" * 130 + "\n"
        for resultado in resultados:
            plagio_title = resultado[0]
            copia = "Si" if resultado[2] > 0.8 else "No"
            original_title = resultado[1]
            similarity_score = resultado[2] * 100  # Convertir a porcentaje
            tipo_plagio = str(resultado[3])
            output += "{:<50} | {:<10} | {:<50} | {:<7.2f} | {:<20}\n".format(
                plagio_title, copia, original_title, similarity_score, tipo_plagio)
        return output

    def generar_documentos_pdf(self, folder_path_plagiados: str, folder_path_original: str,
                               resultados: List[List[Any]]) -> List[List[Any]]:
        """
        Esta funcion recibe dos rutas y los resultados y manda a crear los documentos PDF
        Args: folder_path_plagiados: str, folder_path_original: str, resultados: List[List[Any]]
        Returns: List[List[Any]]
        """
        resultados_finales: List[List[Any]] = []
        total_TP: int = 0
        total_FP: int = 0
        total_TN: int = 0
        total_FN: int = 0

        for titulo in resultados:
            sentences_originales = self.buscar_y_tokenizar(folder_path_original, titulo[1])
            sentences_plagiados = self.buscar_y_tokenizar(folder_path_plagiados, titulo[0])

            if sentences_originales and sentences_plagiados:
                similitud = titulo[2]
                coincidencias, matriz_auc = self.encontrar_coincidencias(sentences_originales, sentences_plagiados)

                total_TP += matriz_auc['TP']
                total_FP += matriz_auc['FP']
                total_TN += matriz_auc['TN']
                total_FN += matriz_auc['FN']

                resultados_finales.append(
                    [
                        f"Similitud entre '{titulo[0]}' y '{titulo[1]}': {similitud * 100:.2f}%",
                        f"Coincidencias para '{titulo[0]}' y '{titulo[1]}':",
                        f"Coincidencias: {coincidencias}"
                    ]
                )

                self.crear_documento_pdf(titulo, similitud, coincidencias)

        TPR = total_TP / (total_TP + total_FN) if (total_TP + total_FN) != 0 else 0
        FPR = total_FP / (total_FP + total_TN) if (total_FP + total_TN) != 0 else 0
        AUC = (1 + TPR - FPR) / 2

        resultados_finales.append(
            [
                f"TPR (Tasa de Verdaderos Positivos): {TPR:.2f}",
                f"FPR (Tasa de Falsos Positivos): {FPR:.2f}",
                f"AUC (Área bajo la curva ROC): {AUC:.2f}"
            ]
        )

        return resultados_finales
