import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import nltk
import os
import gensim.downloader as api
import re

nltk.download('wordnet')

# Carga del modelo GloVe pre-entrenado
word_vectors = api.load("glove-wiki-gigaword-100")

# Función para obtener el embedding de una palabra
def get_word_embedding(word):
    try:
        embedding = word_vectors[word]
    except KeyError:
        embedding = np.zeros(word_vectors.vector_size)  # Si la palabra no está en el vocabulario, devuelve un vector de ceros
    return embedding

# Función para preprocesar los textos
def pre_process(folder_path, ngram, method):
    texto_preprocesado = []
    for fileid in os.listdir(folder_path):
        if fileid.endswith(".txt"):
            filepath = os.path.join(folder_path, fileid)
            with open(filepath, 'r', encoding='latin1', errors='ignore') as file:
                text = file.read()
                palabras = remove_stopwords(text)
                palabras = palabras.split()
                grams = ngram(palabras, ngram)
                texto_preprocesado.append((fileid, [' '.join(ng) for ng in grams]))
    return texto_preprocesado

# Función para eliminar stopwords
def remove_stopwords(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
    text_lista = []
    for palabra in palabras:
        if palabra not in stopwords:
            text_lista.append(palabra)
    nuevo_texto = ' '.join(text_lista)
    return nuevo_texto

# Obtener n-gramas preprocesados para textos plagiados
folder_path_plagiados = "../../textos_plagiados"
preprocess_plagiados = pre_process(folder_path_plagiados, 3, 'lemmatize')

# Obtener n-gramas preprocesados para textos originales
folder_path_originales = "../../docs_originales"
preprocess_originales = pre_process(folder_path_originales, 3, 'lemmatize')

# Combine los n-gramas de los textos plagiados y originales
all_ngrams = preprocess_plagiados + preprocess_originales
labels = [1] * len(preprocess_plagiados) + [0] * len(preprocess_originales)  # 1 para plagiados, 0 para originales

# Construye un vocabulario
vocab = set()
for _, ngrams in all_ngrams:
    vocab.update(ngrams)

# Asigna un índice único a cada n-grama
word_index = {word: idx for idx, word in enumerate(vocab)}

# Convierte n-gramas a secuencias de índices
X = [[word_index[word] for word in ngrams] for _, ngrams in all_ngrams]

# Padding para que todas las secuencias tengan la misma longitud
max_length = max(len(seq) for seq in X)
X_padded = pad_sequences(X, maxlen=max_length, padding='post')

# División de los datos en conjuntos de entrenamiento, validación y prueba
X_train, X_temp, y_train, y_temp = train_test_split(X_padded, labels, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Tamaño del vocabulario
vocab_size = len(vocab)

# Dimensión de los embeddings
embedding_dim = word_vectors.vector_size

# Diseño del modelo
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim),
    LSTM(units=64),
    Dense(units=1, activation='sigmoid')
])

# Compilación del modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenamiento del modelo
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# Evaluación del modelo
loss, accuracy = model.evaluate(X_test, y_test)
print("Accuracy:", accuracy)
