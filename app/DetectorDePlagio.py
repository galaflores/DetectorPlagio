from Data import Data


class DetectorDePlagio(Data):
    def __init__(self):
        super().__init__()
        self.texto_stems = []

    def preprocesar_texto(self, archivo: str) -> list:
        """
        Esta funcion recibe un strig con la ruta del archivo y devuelve una lista con los ngramas del texto preprocesado
        """
        with open(archivo, "r", encoding="utf-8") as file:
            texto = file.read()
            # TODO: Hablititar la opcion de preprocesamiento deseada (lematizacion o stemming)
            #  y numero de ngramas a usar
            texto_stems = self.get_grams(texto, 3)
        return texto_stems

    @staticmethod
    def deteccion_de_plagio(texto):
        """
        Esta función recibe el texto preprocesadio y aplica el modelo de detección de plagio entre el texto preprocesado
        y el texto de los archivos de la base de datos
        """
        # Eliminar signos de puntuación
        texto = texto.replace(".", "").replace(",", "").replace(";", "").replace(":", "").replace("!", "").replace("?",
                                                                                                                   "")
        # Convertir el texto a minúsculas
        texto = texto.lower()

        return texto
