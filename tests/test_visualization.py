import unittest
from matrixlab import create_app

class VisualizationTests(unittest.TestCase):
    def test_addition_sequence(self):
        a, b = [[1, -2], [0.5, 4]], [[3, 1], [1.5, -4]]
        response = create_app({'TESTING': True}).test_client().post('/api/matrices/calculate', json={'operacao':'somar','a':a,'b':b})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultado'], [[4,-1],[2,0]])
        visualization = data['visualizacao']
        self.assertEqual(visualization['a'], a)
        self.assertEqual(visualization['b'], b)
        self.assertEqual([(s['linha'],s['coluna']) for s in visualization['etapas']], [(0,0),(0,1),(1,0),(1,1)])
        for step in visualization['etapas']:
            self.assertEqual(step['valor'], data['resultado'][step['linha']][step['coluna']])
        self.assertIsInstance(data['passos'], list)

    def test_subtraction_visualization(self):
        data = create_app({'TESTING': True}).test_client().post('/api/matrices/calculate', json={'operacao':'subtrair','a':[[1,-2]],'b':[[3,-4]]}).get_json()
        self.assertEqual(data['resultado'], [[-2,2]])
        self.assertEqual([s['valor'] for s in data['visualizacao']['etapas']], [-2,2])
        self.assertEqual(data['visualizacao']['tipo'], 'subtrair')

    def test_rectangular_multiplication_stages(self):
        data = create_app({'TESTING': True}).test_client().post('/api/matrices/calculate', json={'operacao':'multiplicar','a':[[1,2,3]],'b':[[4,1],[5,0],[6,-1]]}).get_json()
        self.assertEqual(data['resultado'], [[32,-2]])
        stages = data['visualizacao']['etapas']
        self.assertEqual(len(stages), 8)
        self.assertEqual([s['indice'] for s in stages[:3]], [0,1,2])
        self.assertEqual(stages[3]['valor'], 32)
        self.assertEqual(stages[7]['valor'], -2)
        self.assertEqual(stages[3]['fase'], 'resultado')
        self.assertEqual(stages[4]['coluna'], 1)

    def test_transpose_rectangular_visualization(self):
        a = [[1,2,3], [4,5,6]]
        data = create_app({'TESTING': True}).test_client().post('/api/matrices/calculate', json={'operacao':'transpor','a':a}).get_json()
        self.assertEqual(data['resultado'], [[1,4],[2,5],[3,6]])
        stages = data['visualizacao']['etapas']
        self.assertEqual(len(stages), 6)
        self.assertEqual([(s['linha_transposta'],s['coluna_transposta']) for s in stages], [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)])
        for step in stages:
            self.assertEqual(step['valor'], a[step['linha_original']][step['coluna_original']])
            self.assertEqual(step['valor'], data['resultado'][step['linha_transposta']][step['coluna_transposta']])
        self.assertNotIn('b', data['visualizacao'])

    def calculate(self, operation, matrix):
        response = create_app({'TESTING': True}).test_client().post(
            '/api/matrices/calculate', json={'operacao': operation, 'a': matrix}
        )
        self.assertEqual(response.status_code, 200, response.get_json())
        return response.get_json()

    def test_transpose_across_dimensions(self):
        for rows, columns in [(1, 1), (1, 8), (8, 1), (3, 3), (5, 2), (8, 8)]:
            with self.subTest(rows=rows, columns=columns):
                original = [[j - i * 2.5 for j in range(columns)] for i in range(rows)]
                response = self.calculate('transpor', original)
                self.assertEqual(response['resultado'], [list(row) for row in zip(*original)])
                frames = response['visualizacao']['etapas']
                self.assertEqual(len(frames), rows * columns)
                coordinates = set()
                for frame in frames:
                    i, j = frame['linha_original'], frame['coluna_original']
                    self.assertEqual((frame['linha_transposta'], frame['coluna_transposta']), (j, i))
                    self.assertEqual(frame['valor'], original[i][j])
                    coordinates.add((j, i))
                self.assertEqual(len(coordinates), rows * columns)

    def test_determinant_all_orders(self):
        from math import factorial

        for n in range(1, 9):
            with self.subTest(order=n):
                # Diagonal 1..n with nonzero entries above it, so the product is n!.
                matrix = [[0 if j < i else i + 1 if j == i else i + j + 1
                           for j in range(n)] for i in range(n)]
                response = self.calculate('determinante', matrix)
                self.assertEqual(response['resultado'], factorial(n))
                trace = response['visualizacao']
                methods = {1: 'direto', 2: 'formula_2x2', 3: 'sarrus'}
                self.assertEqual(trace['metodo'], methods.get(n, 'gauss'))
                self.assertEqual(len(trace['etapas']), len(response['passos']))

    def test_diagonal_steps_use_actual_factors(self):
        for n, matrix in [(2, [[1, 2], [3, 4]]), (3, [[5, -3, 2], [7, 1, -4], [2, 3, 4]])]:
            with self.subTest(order=n):
                from math import prod

                response = self.calculate('determinante', matrix)
                trace = response['visualizacao']
                totals = {'positiva': [], 'negativa': []}
                for step in trace['etapas']:
                    if step['tipo'] != 'diagonal':
                        continue
                    factors = [matrix[i][j % n] for i, j in step['celulas']]
                    total = prod(factors)
                    self.assertTrue(step['expressao'].endswith(f'= {total}'))
                    totals[step['sinal']].append(total)
                diagonals = 1 if n == 2 else 3
                self.assertEqual([len(values) for values in totals.values()], [diagonals, diagonals])
                self.assertEqual(response['resultado'], sum(totals['positiva']) - sum(totals['negativa']))

    def test_gauss_swap_and_elimination_snapshots(self):
        matrix = [[2, 1, 0, 0], [-4, 3, 0, 0], [1, 1, 5, 2], [0, 0, 1, 7]]
        response = self.calculate('determinante', matrix)
        self.assertEqual(response['resultado'], 330)
        steps = response['visualizacao']['etapas']
        self.assertEqual(steps[0]['pivo'], [1, 0])
        self.assertEqual(steps[0]['candidatos'], [[i, 0] for i in range(4)])
        self.assertEqual(steps[1]['linhas'], [0, 1])
        self.assertIn('-1', steps[1]['expressao'])
        self.assertEqual(steps[1]['matriz'][0], ['-4', '3', '0', '0'])
        self.assertEqual(steps[2]['tipo'], 'eliminacao')
        self.assertEqual(steps[2]['linha'], 1)
        self.assertEqual(steps[2]['matriz'][1], ['0', '5/2', '0', '0'])
        self.assertIn('-1/2', steps[2]['expressao'])
        self.assertEqual(len(steps[2]['atualizacoes']), 4)
        triangular = steps[-3]
        self.assertEqual(triangular['tipo'], 'triangular')
        self.assertTrue(all(triangular['matriz'][i][j] == '0' for i in range(4) for j in range(i)))
        self.assertEqual(steps[-2]['celulas'], [[i, i] for i in range(4)])
        self.assertIn('(-1)', steps[-1]['expressao'])

    def test_gauss_singular_exact_and_small_nonzero_pivots(self):
        cases = [
            ([[0] * 4 for _ in range(4)], 0, 'singular'),
            ([[.1, .2, .3, .4], [.3, .6, .9, 1.2], [0, 0, 1, 0], [0, 0, 0, 1]], 0, 'singular'),
            ([[1e-60 if i == j else 0 for j in range(4)] for i in range(4)], 1e-240, 'final'),
            ([[1e-80 if i == j else 0 for j in range(4)] for i in range(4)], 1e-320, 'final'),
            ([[1e-100, 0, 0, 0], [0, 1e100, 0, 0], [0, 0, 1e100, 0], [0, 0, 0, 1e-100]], 1, 'final'),
        ]
        for matrix, result, final in cases:
            with self.subTest(result=result, final=final):
                response = self.calculate('determinante', matrix)
                self.assertEqual(response['resultado'], result)
                self.assertEqual(response['visualizacao']['etapas'][-1]['tipo'], final)

    def test_determinant_preserves_integer_beyond_browser_precision(self):
        a = [[100_000_001, 0], [0, 100_000_001]]
        response = self.calculate('determinante', a)
        result = 10_000_000_200_000_001
        self.assertEqual(response['resultado'], result)
        self.assertEqual(response['visualizacao']['resultado_texto'], str(result))

    def test_determinant_outside_json_numeric_range(self):
        client = create_app({'TESTING': True}).test_client()
        for value in [1e-150, 1e150]:
            with self.subTest(value=value):
                a = [[value if i == j else 0 for j in range(4)] for i in range(4)]
                response = client.post('/api/matrices/calculate', json={'operacao': 'determinante', 'a': a})
                self.assertEqual(response.status_code, 422)
                self.assertEqual(response.get_json()['codigo'], 'determinante_fora_da_faixa')
