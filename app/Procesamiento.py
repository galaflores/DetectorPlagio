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