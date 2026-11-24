"""Testes da ligação HTTP/Python, usando retornos simulados, não algoritmos."""
import json
import unittest
from unittest.mock import patch
from matrixlab import create_app


class MatrixApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def post(self, payload):
        return self.client.post("/api/matrices/calculate", json=payload)

    def test_all_operations_dispatch_validated_arguments(self):
        cases = [
            ({"operacao": "somar", "a": [[2]], "b": [[3]]}, "somar", ([[2]], [[3]]), [[5]]),
            ({"operacao": "subtrair", "a": [[2]], "b": [[3]]}, "subtrair", ([[2]], [[3]]), [[-1]]),
            ({"operacao": "multiplicar", "a": [[2, 3]], "b": [[4], [5]]}, "multiplicar", ([[2, 3]], [[4], [5]]), [[23]]),
            ({"operacao": "transpor", "a": [[2, 3]]}, "transpor", ([[2, 3]],), [[2], [3]]),
            ({"operacao": "determinante", "a": [[1, 2], [3, 4]]}, "determinante", ([[1, 2], [3, 4]],), -2),
            ({"operacao": "identidade", "ordem": 2}, "identidade", (2,), [[1, 0], [0, 1]]),
            ({"operacao": "nula", "linhas": 1, "colunas": 2}, "nula", (1, 2), [[0, 0]]),
        ]
        for payload, name, arguments, output in cases:
            with self.subTest(operation=name), patch(f"matrixlab.domain.matrizes.{name}", return_value={"resultado": output, "passos": ["Passo simulado para testar o transporte."]}) as function:
                response = self.post(payload)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["resultado"], output)
                self.assertEqual(len(response.json["passos"]), 1)
                function.assert_called_once_with(*arguments)

    def test_plain_matrix_and_scalar_returns(self):
        for operation, output in [("transpor", [[1, 3], [2, 4]]), ("determinante", -2)]:
            with self.subTest(operation=operation), patch(f"matrixlab.domain.matrizes.{operation}", return_value=output):
                response = self.post({"operacao": operation, "a": [[1, 2], [3, 4]]})
                self.assertEqual(response.status_code, 200)
                self.assertEqual({key: response.json[key] for key in ("operacao", "resultado", "passos")},
                                 {"operacao": operation, "resultado": output, "passos": []})

    def test_pending_operation_is_not_fake_success(self):
        with patch("matrixlab.domain.matrizes.somar", side_effect=NotImplementedError("Soma pendente.")):
            response = self.post({"operacao": "somar", "a": [[1]], "b": [[2]]})
        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.json["codigo"], "nao_implementado")
        self.assertNotIn("resultado", response.json)

    def test_bad_matrices_rejected_before_algorithm(self):
        invalid = [None, [], [1, 2], [[]], [[1], [2, 3]], [[True]], [["3"]], [[None]], [[float("nan")]], [[float("inf")]], [[10 ** 400]], [[0]] * 9, [[0] * 9]]
        for matrix in invalid:
            with self.subTest(matrix=repr(matrix)[:60]), patch("matrixlab.domain.matrizes.transpor") as function:
                response = self.post({"operacao": "transpor", "a": matrix})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json["codigo"], "entrada_invalida")
                function.assert_not_called()

    def test_incompatible_dimensions(self):
        cases = [
            {"operacao": "somar", "a": [[1]], "b": [[1, 2]]},
            {"operacao": "subtrair", "a": [[1]], "b": [[1], [2]]},
            {"operacao": "multiplicar", "a": [[1, 2]], "b": [[1, 2]]},
            {"operacao": "determinante", "a": [[1, 2]]},
            {"operacao": "determinante", "a": [[0] * 9 for _ in range(9)]},
        ]
        for payload in cases:
            with self.subTest(payload=payload), patch(f"matrixlab.domain.matrizes.{payload['operacao']}") as function:
                self.assertEqual(self.post(payload).status_code, 400)
                function.assert_not_called()

    def test_generator_dimensions_reject_invalid_types_and_limits(self):
        for value in [None, True, 0, -1, 9, 2.5, "2"]:
            with self.subTest(value=value):
                self.assertEqual(self.post({"operacao": "identidade", "ordem": value}).status_code, 400)
                self.assertEqual(self.post({"operacao": "nula", "linhas": 2, "colunas": value}).status_code, 400)

    def test_unknown_operation_and_payload(self):
        for payload in [None, [], {}, {"operacao": "inexistente"}, {"operacao": []}, {"operacao": "somar", "a": [[1]]}]:
            with self.subTest(payload=payload):
                response = self.client.post("/api/matrices/calculate", data=json.dumps(payload), content_type="application/json")
                self.assertEqual(response.status_code, 400)

    def test_media_type_and_malformed_json(self):
        self.assertEqual(self.client.post("/api/matrices/calculate", data="texto").status_code, 415)
        response = self.client.post("/api/matrices/calculate", data='{"a":', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["codigo"], "json_invalido")

    def test_oversized_body_has_json_error(self):
        response = self.client.post("/api/matrices/calculate", data=' ' * 1_000_001, content_type="application/json")
        self.assertEqual(response.status_code, 413)
        self.assertTrue(response.is_json)

    def test_invalid_student_return_is_explained(self):
        outputs = [None, "texto", [[True]], [[float("inf")]], [[1, 2]], {"resultado": [[1]], "passos": "texto"}, {"resultado": [[1]], "passos": [2]}]
        for output in outputs:
            with self.subTest(output=output), patch("matrixlab.domain.matrizes.transpor", return_value=output):
                response = self.post({"operacao": "transpor", "a": [[1]]})
                self.assertEqual(response.status_code, 500)
                self.assertEqual(response.json["codigo"], "resultado_invalido")

    def test_determinant_cannot_return_matrix(self):
        with patch("matrixlab.domain.matrizes.determinante", return_value=[[-2]]):
            response = self.post({"operacao": "determinante", "a": [[1, 2], [3, 4]]})
        self.assertEqual(response.json["codigo"], "resultado_invalido")

    def test_programming_error_does_not_expose_traceback(self):
        with patch("matrixlab.domain.matrizes.transpor", side_effect=ZeroDivisionError("private detail")), self.assertLogs(self.app.logger, level="ERROR"):
            response = self.post({"operacao": "transpor", "a": [[1]]})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["codigo"], "falha_calculo")
        self.assertNotIn("private detail", response.get_data(as_text=True))
