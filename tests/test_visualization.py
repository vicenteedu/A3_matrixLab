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
