"""Read-only JSON endpoints available in phase 1."""
from flask import Blueprint, jsonify
from ..domain.examples import demo_graph

api = Blueprint("api", __name__)


@api.get("/health")
def health():
    return jsonify(status="ok", application="MatrixLab", phase=1)


@api.get("/graph/example")
def graph_example():
    return jsonify(demo_graph())
