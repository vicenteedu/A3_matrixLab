"""Canonical demonstration data, not a shortest-path implementation."""


def demo_graph():
    """Return a fresh example; null means no edge and positions are visual only."""
    return {
        "schema_version": 1,
        "directed": False,
        "nodes": [
            {"id": "A", "x": 95, "y": 170},
            {"id": "B", "x": 265, "y": 65},
            {"id": "C", "x": 265, "y": 275},
            {"id": "D", "x": 435, "y": 170},
        ],
        "adjacency": [[0, 4, 10, None], [4, 0, 2, 8], [10, 2, 0, 3], [None, 8, 3, 0]],
        "source": "A",
        "target": "D",
        "reference": {"path": ["A", "B", "C", "D"], "distance": 9},
    }
