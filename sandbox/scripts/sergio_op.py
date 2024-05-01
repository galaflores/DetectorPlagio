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


# %%
def get_lemmatizer(text):
    palabras = remove_stopwords(text)
    palabras = palabras.split()
    text_lista = []
    for palabra in palabras:
        nueva = lemmatizer.lemmatize(palabra)
        text_lista.append(nueva)
    nuevo_texto = ' '.join(text_lista)
    return nuevo_texto


# %%
def get_stemmer(text):
    palabras = remove_stopwords(text)
    palabras = palabras.split()
    text_lista = []
    for palabra in palabras:
        nueva = lancStemmer.stem(palabra)
        text_lista.append(nueva)
    nuevo_texto = ' '.join(text_lista)
    return nuevo_texto


# %%
def get_grams(text, ngram, method):
    result = []

    if method == 'lemmatize':
        text = get_lemmatizer(text)
        if ngram == 0:  # Si ngram es 0, se retorna el texto completo sin ngramas
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
        if ngram == 0:  # Si ngram es 0, se retorna el texto completo sin ngramas
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


# %%
def token_sentence(text):
    sentences = nltk.sent_tokenize(text)
    filtered_sentences = []
    for sentence in sentences:
        filtered_words = remove_stopwords(sentence)
        filtered_sentences.append(filtered_words)

    return filtered_sentences


# %%
# FUNCION QUE INCLUYE EL USO DE NGRAMAS
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


# Preprocessing function for documents
# Preprocessing function for documents
# Preprocessing function for documents
# Preprocessing function for documents
def preprocess_docs(folder_path, ngram, method):
    """
    Preprocesses the documents in the given folder path.
    """
    tagged_documents = []
    for fileid in os.listdir(folder_path):
        if fileid.endswith(".txt"):
            filepath = os.path.join(folder_path, fileid)
            with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                text = file.read()
                grams = get_grams(text, ngram, method)
                # Ensure words are split into a list of strings and then converted to tuple
                words = tuple(word.split() for word in grams)
                # Flatten the list of lists into a single list of strings
                words = [word for sublist in words for word in sublist]
                tagged_documents.append(TaggedDocument(words=words, tags=[fileid]))

    return tagged_documents



# %%
# Training Doc2Vec model
def train_doc2vec(tagged_documents):
    """
    Trains the Doc2Vec model with the given tagged documents.
    """
    model = Doc2Vec(vector_size=100, window=5, min_count=1, epochs=200,
                    dm=0)  # dm=0 for distributed bag of words (DBOW) mode
    model.build_vocab(tagged_documents)
    model.train(tagged_documents, total_examples=model.corpus_count, epochs=model.epochs)
    return model


# %%
# Function to calculate similarity between documents using Doc2Vec embeddings
def calculate_similarity_doc2vec(doc1, doc2, model):
    """
    Calculates the similarity between two documents using Doc2Vec embeddings.
    """
    vec1 = model.infer_vector(doc1.words)
    vec2 = model.infer_vector(doc2.words)
    similarity = model.dv.similarity(doc1.tags[0], doc2.tags[0])
    return similarity


# Obtener n-gramas preprocesados
folder_path = "../../textos_plagiados"  # Ruta de la carpeta con los textos plagiados)
folder_path_og = "../../docs_originales"  # Ruta de la carpeta con los textos originales


# Preprocessing original and plagiarized documents
tagged_originals = preprocess_docs(folder_path_og, 2, 'lemmatize')
tagged_plagiarized = preprocess_docs(folder_path, 2, 'lemmatize')

# Training the Doc2Vec model
model = train_doc2vec(tagged_originals + tagged_plagiarized)

# List to store similarity results
similarity_results = []

# Iterating over each plagiarized text
for plagio_doc in tagged_plagiarized:
    max_similarity = 0
    most_similar = ''
    most_similar_doc = ''

    # Comparing with each original document
    for original_doc in tagged_originals:
        similarity = calculate_similarity_doc2vec(plagio_doc, original_doc, model)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar = original_doc.tags[0]
            most_similar_doc = original_doc.words

    similarity_results.append([plagio_doc.tags[0], most_similar, max_similarity, most_similar_doc])

# Sorting results by similarity in descending order
similarity_results.sort(key=lambda x: x[2], reverse=True)

# Printing results
for result in similarity_results:
    plagio_title, original_title, similarity_score, original_doc = result
    print(f"Similarity between '{plagio_title}' and '{original_title}': {similarity_score * 100:.2f}%")