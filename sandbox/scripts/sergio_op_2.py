import numpy as np
import nltk
import os
import difflib
from gensim.models import Word2Vec
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from nltk.util import ngrams
import gensim.downloader as api
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
nltk.download('punkt')

lemmatizer = WordNetLemmatizer() #lemmatizer algorithm
lancStemmer = LancasterStemmer()  # stemming algorithm Lancaster


def remove_stopwords(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
    text_lista = []
    for palabra in palabras:
        if palabra not in stopwords:
            text_lista.append(palabra)
    nuevo_texto = ' '.join(text_lista)
    return nuevo_texto


def get_lemmatizer(text):
    palabras = remove_stopwords(text)
    palabras = palabras.split()
    text_lista = []
    for palabra in palabras:
        nueva = lemmatizer.lemmatize(palabra)
        text_lista.append(nueva)
    nuevo_texto = ' '.join(text_lista)
    return nuevo_texto


def get_stemmer(text):
    palabras = remove_stopwords(text)
    palabras = palabras.split()
    text_lista = []
    for palabra in palabras:
        nueva = lancStemmer.stem(palabra)
        text_lista.append(nueva)
    nuevo_texto = ' '.join(text_lista)
    return nuevo_texto


def get_grams(text, ngram, method):
    result = []

    if method == 'lemmatize':
        text = get_lemmatizer(text)
        if ngram == 0:
            text = nltk.sent_tokenize(text)
            text = ' '.join(text)
            return text

        else:
            text = text.split()
            grams = ngrams(text, ngram)
            for ng in grams:
                result.append(' '.join(ng))
    elif method == 'stemmer':
        text = get_stemmer(text)
        if ngram == 0:
            text = nltk.sent_tokenize(text)
            text = ' '.join(text)
            return text

        else:
            text = text.split()
            grams = ngrams(text, ngram)
            for ng in grams:
                result.append(' '.join(ng))
    else:
        raise ValueError('Method not found')

    return result


def token_sentence(text):
    sentences = nltk.sent_tokenize(text)
    filtered_sentences = []
    for sentence in sentences:
        filtered_words = remove_stopwords(sentence)
        filtered_sentences.append(filtered_words)

    return filtered_sentences


def pre_process(folder_path, ngram, method):
    texto_preprocesado = []
    for fileid in os.listdir(folder_path):
        if fileid.endswith(".txt"):
            filepath = os.path.join(folder_path, fileid)
            with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                text = file.read()
                grams = get_grams(text, ngram, method)
                texto_preprocesado.append((fileid, grams))

    return texto_preprocesado


def preprocess_docs(folder_path, ngram, method):
    tagged_documents = []
    for fileid in os.listdir(folder_path):
        if fileid.endswith(".txt"):
            filepath = os.path.join(folder_path, fileid)
            with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                text = file.read()
                grams = get_grams(text, ngram, method)
                words = tuple(word.split() for word in grams)
                words = [word for sublist in words for word in sublist]
                tagged_documents.append(TaggedDocument(words=words, tags=[fileid]))

    return tagged_documents


def train_doc2vec(tagged_documents):
    model = Doc2Vec(vector_size=100, window=5, min_count=1, epochs=200,
                    dm=0)  # dm=0 for distributed bag of words (DBOW) mode
    model.build_vocab(tagged_documents)
    model.train(tagged_documents, total_examples=model.corpus_count, epochs=model.epochs)
    return model


def calculate_similarity_doc2vec(doc1, doc2, model):
    vec1 = model.infer_vector(doc1.words)
    vec2 = model.infer_vector(doc2.words)
    similarity = model.dv.similarity(doc1.tags[0], doc2.tags[0])
    return similarity


def print_plagiarism(original_sentence, plagiarized_sentence):
    print("Coincidencias para el plagio:")
    print("----------------------------")
    print(f"Cadena original: {original_sentence} (Longitud: {len(original_sentence)})")
    print(f"Cadena plagiada: {plagiarized_sentence}")
    print()



def detect_plagiarism_type(original_doc, plagiarized_doc):
    # Comparing lengths to detect insertion or replacement
    if len(plagiarized_doc) > len(original_doc):
        print("Plagiarism type: Insertion or Replacement")
    else:
        # Comparing if sentences are shuffled
        if original_doc != plagiarized_doc:
            print("Plagiarism type: Sentence Shuffle")
        else:
            # You can implement more sophisticated methods to detect other types of plagiarism
            print("Plagiarism type: Unknown")


folder_path = "../../textos_plagiados"
folder_path_og = "../../docs_originales"

tagged_originals = preprocess_docs(folder_path_og, 2, 'lemmatize')
tagged_plagiarized = preprocess_docs(folder_path, 2, 'lemmatize')

model = train_doc2vec(tagged_originals + tagged_plagiarized)

similarity_results = []

for plagio_doc in tagged_plagiarized:
    max_similarity = 0
    most_similar = ''
    most_similar_doc = ''

    for original_doc in tagged_originals:
        similarity = calculate_similarity_doc2vec(plagio_doc, original_doc, model)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar = original_doc.tags[0]
            most_similar_doc = original_doc.words

    similarity_results.append([plagio_doc.tags[0], most_similar, max_similarity, most_similar_doc])

similarity_results.sort(key=lambda x: x[2], reverse=True)


for result in similarity_results:
    plagio_title, original_title, similarity_score, original_doc = result
    print(f"Titulo: {plagio_title}")
    print(f"Similitud entre '{plagio_title}' y '{original_title}': {similarity_score * 100:.2f}%")
    # Retrieve original and plagiarized documents by title
    original_doc_text = ' '.join([word for word in original_doc])
    plagiarized_doc_text = [doc.words for doc in tagged_plagiarized if doc.tags[0] == plagio_title][0]
    plagiarized_doc_text = ' '.join([word for word in plagiarized_doc_text])
    print_plagiarism(original_doc_text, plagiarized_doc_text)
    detect_plagiarism_type(original_doc_text, plagiarized_doc_text)