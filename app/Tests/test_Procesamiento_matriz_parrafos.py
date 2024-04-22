from app.Procesamiento import Procesamiento
import pytest


class TestMatrizParrafos:

    # Devuelve una lista de listas con la misma longitud que grams_juntos
    def test_same_length(self):
        grams1 = ['palabra1', 'palabra2', 'palabra3']
        grams2 = ['palabra4', 'palabra5', 'palabra6']
        longitud_esperada = 2

        resultado = Procesamiento.matriz_parrafos(grams1, grams2)

        assert len(resultado) == longitud_esperada

    # Funciona correctamente con entradas que contienen listas vacías
    def test_empty_lists(self):
        grams1 = ['palabra1', 'palabra2', 'palabra3']
        grams2 = []
        resultado_esperado = [[1, 1, 1], [0, 0, 0]]

        resultado = Procesamiento.matriz_parrafos(grams1, grams2)

        assert resultado == resultado_esperado

    # La salida solo contiene 1s y 0s
    def test_only_ones_and_zeros(self):
        grams1 = ['palabra1', 'palabra2', 'palabra3']
        grams2 = ['palabra4', 'palabra5', 'palabra6']

        resultado = Procesamiento.matriz_parrafos(grams1, grams2)

        for fila in resultado:
            for elemento in fila:
                assert elemento == 0 or elemento == 1

    # La salida es determinista para una entrada dada
    def test_deterministic_output(self):
        grams1 = ['palabra1', 'palabra2', 'palabra3']
        grams2 = ['palabra4', 'palabra5', 'palabra6']

        resultado1 = Procesamiento.matriz_parrafos(grams1, grams2)
        resultado2 = Procesamiento.matriz_parrafos(grams1, grams2)

        assert resultado1 == resultado2
