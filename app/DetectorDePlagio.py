from typing import List, Any
import Preprocesamineto
import Procesamiento
from sklearn.metrics.pairwise import cosine_similarity


class DetectorDePlagio(Preprocesamineto.Preprocesamiento, Procesamiento.Procesamiento):
    def __init__(self):
        super().__init__()
        self.texto_stems = []
        self.archivo_texto_stems = []

    def preprocesar_texto(self, ruta: str, is_archivo: bool) -> list:
        """
        Esta funcion recibe una ruta y el tipo (si es archivo o carpeta) y manda a preprocesar el texto
        """
        if not is_archivo:
            return self.pre_procesados(ruta, 3)
        else:
            # Procesar un archivo individualmente
            with open(ruta, 'r', encoding='latin1', errors='ignore') as file:
                text = file.read()
                grams = self.get_grams(text, 3)
            return grams

    def analizar_similitud(self, folder_path_plagiados: str, folder_path_originales: str) -> List[List[Any]]:

        preprocess_plagiados = self.preprocesar_texto(folder_path_plagiados, False)
        preprocess_originales = self.preprocesar_texto(folder_path_originales, False)

        resultados = []
        for id_plagiado, (name_plagiado, grams_plagiado) in enumerate(preprocess_plagiados, 1):
            for id_original, (name_original, grams_original) in enumerate(preprocess_originales, 1):
                similitud = cosine_similarity(self.matriz_parrafos(grams_plagiado, grams_original))
                if similitud[0][1] != 0.0 and similitud[0][1] >= 0.2:
                    resultados.append([name_plagiado, name_original, similitud[0][1]])

        resultados.sort(key=lambda x: x[2], reverse=True)

        return resultados

    def generar_documentos_pdf(self, folder_path_plagiados: str, folder_path_og: str,
                               resultados: List[List[Any]]) -> List[List[Any]]:
        resultados_finales = []
        for titulo in resultados:
            sentences_originales = self.buscar_y_tokenizar(folder_path_og, titulo[1])
            sentences_plagiados = self.buscar_y_tokenizar(folder_path_plagiados, titulo[0])

            if sentences_originales and sentences_plagiados:
                similitud = titulo[2]
                coincidencias = self.encontrar_coincidencias(sentences_originales, sentences_plagiados)
                resultados_finales.append(
                    [
                        f"Similitud entre '{titulo[0]}' y '{titulo[1]}': {similitud * 100:.2f}%",
                        f"Coincidencias para '{titulo[0]}' y '{titulo[1]}':",
                        f"Coincidencias: {coincidencias}"
                    ]
                )
                # TODO: Regresar el porcentaje total de similitud y en que documento hubo mayor similitud

                # llamar a la función para crear el documento PDF
                self.crear_documento_pdf(titulo, similitud, coincidencias)

        return resultados_finales
