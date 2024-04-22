from typing import List, Tuple, Any
import Preprocesamineto
import Procesamiento
from sklearn.metrics.pairwise import cosine_similarity
import os


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
