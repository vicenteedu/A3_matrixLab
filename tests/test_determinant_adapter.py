import copy
import unittest
from unittest.mock import patch

from matrixlab import create_app
from matrixlab.domain import matrizes
from matrixlab.domain.determinant_visualization import visualizar_determinante


class DeterminantAdapterTests(unittest.TestCase):
    def test_animation_preserves_student_result_steps_and_inputs(self):
        client = create_app({"TESTING": True}).test_client()
        cases = []
        for n in range(1, 9):
            triangular = [[i + 1 if i == j else 2 if j > i else 0
                           for j in range(n)] for i in range(n)]
            cases.append(triangular)
            if n > 1:
                swapped = copy.deepcopy(triangular)
                swapped[0], swapped[-1] = swapped[-1], swapped[0]
                cases.append(swapped)
            cases.append([[0] * n for _ in range(n)])
        cases.append([[2, 1, 0, 0], [-4, 3, 0, 0], [1, 1, 5, 2], [0, 0, 1, 7]])
        for matrix in cases:
            with self.subTest(matrix=matrix):
                original = copy.deepcopy(matrix)
                expected = matrizes.determinante(matrix)
                response = client.post('/api/matrices/calculate', json={
                    'operacao': 'determinante', 'a': matrix})
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertEqual(data['resultado'], expected['resultado'])
                self.assertEqual(data['passos'], expected['passos'])
                self.assertTrue(data['visualizacao']['etapas'])
                self.assertEqual(data['visualizacao']['versao'], 1)
                self.assertEqual(matrix, original)

    def test_gauss_frames_match_native_arithmetic(self):
        matrix = [[2, 1, 0, 0], [-4, 3, 0, 0], [1, 1, 5, 2], [0, 0, 1, 7]]
        trace = visualizar_determinante(matrix, matrizes.determinante(matrix)['resultado'])
        previous = copy.deepcopy(matrix)
        for frame in trace['etapas']:
            if frame['tipo'] == 'troca':
                i, j = frame['linhas']
                previous[i], previous[j] = previous[j], previous[i]
            elif frame['tipo'] == 'eliminacao':
                k, _ = frame['pivo']
                i = frame['linha']
                factor = previous[i][k] / previous[k][k]
                for j in range(k, len(matrix)):
                    previous[i][j] -= factor * previous[k][j]
            if 'matriz' in frame:
                self.assertEqual(frame['matriz'], [[str(x) for x in row] for row in previous])

    def test_mismatch_does_not_change_result_or_invent_animation(self):
        self.assertIsNone(visualizar_determinante([[1]], 99))

    def test_existing_visualization_is_preserved(self):
        raw = {'resultado': 1, 'passos': ['original'], 'visualizacao': {'custom': True}}
        with patch.object(matrizes, 'determinante', return_value=raw):
            response = create_app({'TESTING': True}).test_client().post(
                '/api/matrices/calculate', json={'operacao': 'determinante', 'a': [[1]]})
        self.assertEqual(response.get_json()['visualizacao'], raw['visualizacao'])
