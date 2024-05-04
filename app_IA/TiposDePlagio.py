import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from difflib import SequenceMatcher

class TiposDePlagio:
    @staticmethod
    def detector_cambio_voz(oracion_original, oracion_plagiada):
        """
        Detecta si hay cambio de voz entre dos oraciones al identificar si el sujeto de la oración cambió
        en la oración plagiada respecto a la oración original.
        """
        original_tags = nltk.pos_tag(word_tokenize(oracion_original))
        plagio_tags = nltk.pos_tag(word_tokenize(oracion_plagiada))

        # Identificar el sujeto en ambas oraciones
        for (word_orig, tag_orig), (word_plag, tag_plag) in zip(original_tags, plagio_tags):
            if tag_orig.startswith('VB') and tag_plag.startswith('VB'):
                if word_orig.lower() != word_plag.lower():  # Verificar si el verbo cambió
                    return True  # Hay cambio de voz
        return False  # No hay cambio de voz

    @staticmethod
    def detectar_reorganizacion(sentences_originales, sentences_plagiados, umbral_similitud=0.8):
        """
        Detecta reorganización de oraciones comparando la similitud entre las oraciones originales y plagiadas.
        """
        for sentence_orig, sentence_plagiada in zip(sentences_originales, sentences_plagiados):
            sentence_orig_text = ' '.join(sentence_orig.words)
            sentence_plagiada_text = ' '.join(sentence_plagiada.words)
            similitud = SequenceMatcher(None, sentence_orig_text, sentence_plagiada_text).ratio()
            if similitud >= umbral_similitud:
                return True  # Hay reorganización
        return False  # No hay reorganización

    @staticmethod
    def detectar_cambio_tiempo(oracion_original, oracion_plagiada):
        """
        Esta función detecta si hay un cambio de tiempo verbal en la oración plagiada en comparación con la original.
        Devuelve True si hay un cambio de tiempo verbal, de lo contrario, devuelve False.
        """
        # Inicializar lematizador y lista de stopwords
        lemmatizer = WordNetLemmatizer()
        stop_words = set(nltk.corpus.stopwords.words('english'))

        # Tokenizar las oraciones
        tokens_original = word_tokenize(oracion_original)
        tokens_plagiada = word_tokenize(oracion_plagiada)

        # Lematizar y filtrar palabras
        lemmatized_original = [lemmatizer.lemmatize(word) for word in tokens_original if
                               word.isalnum() and word.lower() not in stop_words]
        lemmatized_plagiada = [lemmatizer.lemmatize(word) for word in tokens_plagiada if
                               word.isalnum() and word.lower() not in stop_words]

        # Etiquetar las palabras de ambas oraciones con sus partes del discurso (POS)
        tags_original = pos_tag(lemmatized_original)
        tags_plagiada = pos_tag(lemmatized_plagiada)

        # Extraer los verbos de cada oración
        verbos_original = [palabra for palabra, etiqueta in tags_original if etiqueta.startswith('VB')]
        verbos_plagiada = [palabra for palabra, etiqueta in tags_plagiada if etiqueta.startswith('VB')]

        # Verificar si hay cambios de tiempo verbal comparando los verbos de ambas oraciones
        if verbos_original and verbos_plagiada:
            tiempo_original = nltk.pos_tag(verbos_original)[0][1]
            tiempo_plagiada = nltk.pos_tag(verbos_plagiada)[0][1]
            return tiempo_original != tiempo_plagiada
        else:
            # Si no hay verbos en alguna de las oraciones, no se puede determinar un cambio de tiempo verbal
            return False

    @staticmethod
    def detectar_parafraseo(oracion_original, oracion_plagiada, umbral_similitud=0.8):
        """
        Esta función detecta si el tipo de plagio es parafraseo comparando la similitud entre las oraciones original y plagiada.
        Devuelve True si la similitud es mayor o igual al umbral especificado, de lo contrario, devuelve False.
        """
        # Calcular la similitud entre las oraciones original y plagiada
        similitud = SequenceMatcher(None, oracion_original, oracion_plagiada).ratio()

        # Comprobar si la similitud supera el umbral especificado
        return similitud >= umbral_similitud

    @staticmethod
    def detectar_insertar_reemplazar(oracion_original, oracion_plagiada, umbral_palabras_comunes=0.8,
                                     umbral_longitud=0.5):
        """
        Esta función detecta si el tipo de plagio implica la inserción o reemplazo de frases del documento original en el documento plagiado.
        Devuelve True si la proporción de palabras comunes entre las oraciones supera el umbral especificado y la longitud de la oración plagiada es significativamente mayor que la original, de lo contrario, devuelve False.
        """
        # Tokenizar las oraciones en palabras
        palabras_originales = oracion_original.split()
        palabras_plagiadas = oracion_plagiada.split()

        # Calcular la proporción de palabras comunes
        palabras_comunes = set(palabras_originales) & set(palabras_plagiadas)
        prop_palabras_comunes = len(palabras_comunes) / len(set(palabras_originales))

        # Calcular la longitud relativa de la oración plagiada con respecto a la original
        long_orig = len(palabras_originales)
        long_plagiada = len(palabras_plagiadas)
        prop_longitud = long_plagiada / long_orig

        # Comprobar si la proporción de palabras comunes supera el umbral y la longitud de la oración plagiada es significativamente mayor que la original
        return prop_palabras_comunes >= umbral_palabras_comunes and prop_longitud >= umbral_longitud
