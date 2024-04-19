from typing import Tuple, Any

from Data import Data
import os


class DetectorDePlagio(Data):
    def __init__(self):
        super().__init__()
        self.texto_stems = []
        self.archivo_texto_stems = []

    def preprocesar_texto(self, archivo: str, ruta: str) -> list:
        """
        Esta funcion recibe un strig con la ruta del archivo y devuelve una lista con los ngramas del texto preprocesado
        """

        # Importa los archivos de la base de datos y los manda a preprocesar
        for filename in os.listdir(ruta):
            if filename.endswith(".txt"):
                with open(os.path.join(ruta, filename), 'r') as f:
                    texto = f.read()
                    archivo_texto_stems = self.get_grams(texto, 3)
                    self.archivo_texto_stems.append(archivo_texto_stems)

        # Importar el archivo seleccionado y mandarlo a preprocesar
        with open(archivo, "r", encoding="utf-8") as file:
            texto = file.read()
            # TODO: Hablititar la opcion de preprocesamiento deseada (lematizacion o stemming)
            #  y numero de ngramas a usar
            self.texto_stems = self.get_grams(texto, 3)

        # Suma el resultado del preprocesamiento a la base de datos y del archivo
        return [self.texto_stems] + [self.archivo_texto_stems]

    # TODO: Habilitar la deteccion de plagio
    @staticmethod
    def deteccion_de_plagio(self, texto_preprocesado, option):
        """
        Esta función recibe el texto preprocesadio y aplica el modelo de detección de plagio entre el texto preprocesado
        y el texto de los archivos de la base de datos
        """
        return texto_preprocesado
