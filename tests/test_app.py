"""Phase 1 integration and example-contract tests. Run with unittest discovery."""
import unittest
from matrixlab import create_app
from matrixlab.domain.examples import demo_graph


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app({"TESTING": True}).test_client()

    def test_home_and_local_assets(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('lang="pt-BR"', response.get_data(as_text=True))
        for filename in ("css/app.css", "js/app.js", "js/icons.js", "js/graph-view.js", "js/matrix-editor.js", "favicon.svg"):
            with self.subTest(asset=filename):
                with self.client.get(f"/static/{filename}") as asset:
                    self.assertEqual(asset.status_code, 200)

    def test_health_contract(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"application": "MatrixLab", "phase": 1, "status": "ok"})

    def test_example_endpoint(self):
        response = self.client.get("/api/graph/example")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.json, demo_graph())

    def test_missing_api_returns_json_error(self):
        response = self.client.get("/api/missing")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"]["code"], "not_found")

    def test_missing_page_has_return_link(self):
        response = self.client.get("/missing")
        self.assertEqual(response.status_code, 404)
        self.assertIn('href="/"', response.get_data(as_text=True))


class ExampleContractTests(unittest.TestCase):
    def test_undirected_positive_example(self):
        graph = demo_graph()
        self.assertFalse(graph["directed"])
        self.assertEqual([node["id"] for node in graph["nodes"]], list("ABCD"))
        matrix = graph["adjacency"]
        self.assertEqual(len(matrix), len(graph["nodes"]))
        for i, row in enumerate(matrix):
            self.assertEqual(len(row), len(matrix))
            self.assertEqual(row[i], 0)
            for j, weight in enumerate(row):
                self.assertEqual(weight, matrix[j][i])
                if i != j and weight is not None:
                    self.assertGreater(weight, 0)

    def test_exact_requested_edges_and_reference(self):
        graph = demo_graph()
        self.assertEqual(graph["adjacency"], [[0, 4, 10, None], [4, 0, 2, 8], [10, 2, 0, 3], [None, 8, 3, 0]])
        self.assertEqual(graph["reference"], {"path": list("ABCD"), "distance": 9})
        # Verify the stated route's cost, without asserting that Dijkstra exists.
        self.assertEqual(sum(graph["adjacency"][i][i + 1] for i in range(3)), 9)

    def test_examples_do_not_share_mutable_state(self):
        changed = demo_graph()
        changed["adjacency"][0][1] = 99
        changed["nodes"][0]["x"] = 0
        self.assertEqual(demo_graph()["adjacency"][0][1], 4)
        self.assertEqual(demo_graph()["nodes"][0]["x"], 95)

    def test_positions_do_not_determine_weights(self):
        graph = demo_graph()
        original_weights = [row[:] for row in graph["adjacency"]]
        graph["nodes"][0].update(x=500, y=500)
        self.assertEqual(graph["adjacency"], original_weights)


if __name__ == "__main__":
    unittest.main()
