"""Exercícios de aceitação: ficam SKIPPED enquanto a função está pendente.

Ao implementar uma função de matrizes.py, seu teste passa a verificar a resposta.
Estes testes não usam mocks e não implementam os algoritmos por vocês.
"""
import unittest
from matrixlab.domain import matrizes


class ResolucaoDasMatrizesTests(unittest.TestCase):
    def resolve(self, function, *arguments):
        try:
            result = function(*arguments)
        except NotImplementedError:
            self.skipTest(f"Implementar {function.__name__} em matrizes.py")
        return result.get("resultado") if isinstance(result, dict) else result

    def test_somar(self):
        self.assertEqual(self.resolve(matrizes.somar, [[1, -2], [3, 4]], [[5, 2], [-3, 6]]), [[6, 0], [0, 10]])

    def test_subtrair(self):
        self.assertEqual(self.resolve(matrizes.subtrair, [[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[-4, -4], [-4, -4]])

    def test_multiplicar_retangulares(self):
        self.assertEqual(self.resolve(matrizes.multiplicar, [[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]]), [[58, 64], [139, 154]])

    def test_transpor_retangular(self):
        self.assertEqual(self.resolve(matrizes.transpor, [[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])

    def test_determinante_2x2(self):
        self.assertEqual(self.resolve(matrizes.determinante, [[1, 2], [3, 4]]), -2)

    def test_determinante_3x3(self):
        self.assertEqual(self.resolve(matrizes.determinante, [[1, 2, 3], [0, 1, 4], [5, 6, 0]]), 1)

    def test_determinante_singular(self):
        self.assertEqual(self.resolve(matrizes.determinante, [[1, 2], [2, 4]]), 0)

    def test_identidade(self):
        self.assertEqual(self.resolve(matrizes.identidade, 3), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_nula_retangular(self):
        self.assertEqual(self.resolve(matrizes.nula, 2, 3), [[0, 0, 0], [0, 0, 0]])

    def test_somar_decimais(self):
        self.assertEqual(self.resolve(matrizes.somar, [[1.5]], [[2.25]]), [[3.75]])
