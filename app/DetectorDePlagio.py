from Data import Data


class DetectorDePlagio(Data):
    def __init__(self):
        super().__init__()
        self.texto_stems = []

    def preprocesar_texto(self, archivo):
        """
        Esta función recibe la ruta de un archivo de texto y devuelve el contenido del archivo preprocesado.
        """
        with open(archivo, "r", encoding="utf-8") as file:
            texto = file.read()
            texto_stems = self.get_grams(texto, 3)
        return texto_stems

    @staticmethod
    def deteccion_de_plagio(texto):
        """
        Esta función recibe un texto y devuelve el texto preprocesado.
        """
        # Eliminar signos de puntuación
        texto = texto.replace(".", "").replace(",", "").replace(";", "").replace(":", "").replace("!", "").replace("?",
                                                                                                                   "")
        # Convertir el texto a minúsculas
        texto = texto.lower()

        return texto
