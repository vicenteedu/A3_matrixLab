"""Endpoints JSON do laboratório."""
from flask import Blueprint, jsonify
from ..domain.examples import demo_graph
from .matrices import calculate_matrix

api = Blueprint("api", __name__)
api.add_url_rule("/matrices/calculate", view_func=calculate_matrix, methods=["POST"])


@api.get("/health")
def health():
    return jsonify(status="ok", application="MatrixLab", phase=1)


@api.get("/graph/example")
def graph_example():
    return jsonify(demo_graph())
