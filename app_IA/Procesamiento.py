import difflib
from typing import List, Dict, Any, Tuple

from gensim.models import Doc2Vec

from Preprocesamineto import Preprocesamiento
import os
from fpdf import FPDF
import TiposDePlagio


class Procesamiento(TiposDePlagio.TiposDePlagio):
    """
    Esta clase contiene funciones para procesar los textos y encontrar coincidencias
    """
    def train_doc2vec(self, tagged_documents: List[Tuple[str, List[str]]]) -> Doc2Vec:
        model = Doc2Vec(vector_size=80, window=5, min_count=1, epochs=200, dm=0)  # dm=0 for distributed bag of words (DBOW) mode
        model.build_vocab(tagged_documents)
        model.train(tagged_documents, total_examples=model.corpus_count, epochs=model.epochs)
        return model

    def calculate_similarity_doc2vec(self, doc1, doc2, model: Doc2Vec) -> float:
        similarity = model.dv.similarity(doc1.tags[0], doc2.tags[0])
        return similarity

    def encontrar_coincidencias(self, sentences_originales: List[str], sentences_plagiados: List[str],
                                model: Doc2Vec) -> Tuple[List[Dict[str, Any]], Dict[str, int], List[str]]:
        coincidencias: List[Dict[str, Any]] = []
        tipo_plagio: Dict[str, int] = {'Cambio de voz': 0, 'Desorden de oraciones': 0, 'Cambio de tiempo verbal': 0,
                                       'Parafraseo': 0,
                                       'Inserción o reemplazo': 0}
        TP: int = 0
        FP: int = 0
        TN: int = 0
        FN: int = 0

        for sentence_orig in sentences_originales:
            tiene_coincidencia = False
            for sentence_plag in sentences_plagiados:
                similarity = self.calculate_similarity_doc2vec(sentence_orig, sentence_plag, model)
                if similarity > 0.6 and abs(len(sentence_orig) - len(sentence_plag)) < 15:
                    coincidencias.append({
                        "cadena_orig": sentence_orig,
                        "cadena_plag": sentence_plag,
                        "similitud": similarity
                    })
                    if sentence_orig == sentence_plag:
                        TP += 1
                    else:
                        FP += 1
                    tiene_coincidencia = True

                    cambio_voz = self.detector_cambio_voz(' '.join(sentence_orig.words), ' '.join(sentence_plag.words))
                    # print("ORACION ORIGINAL:",' '.join(sentence_orig.words))
                    # print("ORACION PLAGIADA:",' '.join(sentence_plag.words))
                    reorganizacion = self.detectar_reorganizacion(sentences_originales, sentences_plagiados)
                    cambio_tiempo = self.detectar_cambio_tiempo(' '.join(sentence_orig.words),
                                                                ' '.join(sentence_plag.words))
                    parafraseo = self.detectar_parafraseo(' '.join(sentence_orig.words), ' '.join(sentence_plag.words))
                    insertar_reemplazar = self.detectar_insertar_reemplazar(' '.join(sentence_orig.words),
                                                                            ' '.join(sentence_plag.words))
                    if cambio_voz:
                        tipo_plagio['Cambio de voz'] += 1
                    if reorganizacion:
                        tipo_plagio['Desorden de oraciones'] += 1
                    if cambio_tiempo:
                        tipo_plagio['Cambio de tiempo verbal'] += 1
                    if parafraseo:
                        tipo_plagio['Parafraseo'] += 1
                    if insertar_reemplazar:
                        tipo_plagio['Inserción o reemplazo'] += 1

            # print(tipo_plagio)
            if not tiene_coincidencia:
                FN += 1
            else:
                TN += 1
        # Contabilizar tipos de plagio y encontrar el mayor
        plagio_count = tipo_plagio
        # mayor_tipo_plagio = max(plagio_count, key=plagio_count.get)
        max_count = max(plagio_count.values())
        mayor_tipo_plagio = [tipo for tipo, count in plagio_count.items() if count == max_count]

        matriz_auc = {'TP': TP, 'FP': FP, 'TN': TN, 'FN': FN}
        # print(matriz_auc)
        # print(f"Tipos de plagio contabilizados: {plagio_count}")
        # print(f"Mayor tipo de plagio: {mayor_tipo_plagio}")
        return coincidencias, matriz_auc, mayor_tipo_plagio

    @staticmethod
    def crear_documento_pdf(titulo: Tuple[str, str], similitud: float, coincidencias: List[Dict[str, Any]]) -> None:
        """
        Esta función recibe un título, un porcentaje de similitud y una lista de coincidencias y crea un documento PDF
        Args: titulo: Tuple[str, str], similitud: float, coincidencias: List[Dict[str, Any]]
        Returns: None
        
        """
        # Crear un nuevo objeto PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Agregar una página
        pdf.add_page()

        # Establecer la fuente y el tamaño del texto
        pdf.set_font("Arial", size=12)

        # Título del documento
        pdf.cell(200, 10, txt=f"Resultados de prueba de plagio: {titulo}", ln=True, align="C")

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
