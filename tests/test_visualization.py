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
