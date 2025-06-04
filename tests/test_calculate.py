import importlib
import mongomock
import pytest
import pathlib
import sys


def setup_calculate(monkeypatch):
    """Import calculate module with mongomock patched."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    monkeypatch.setattr('pymongo.MongoClient', mongomock.MongoClient)
    module = importlib.import_module('backend.routing.calculate')
    # Reload to ensure patch takes effect if already imported
    module = importlib.reload(module)
    return module


def test_find_route(monkeypatch):
    calculate = setup_calculate(monkeypatch)
    # insert nodes
    calculate.nodes_col.insert_many([
        {'_id': '1', 'lat': 0, 'lng': 0},
        {'_id': '2', 'lat': 0, 'lng': 1},
        {'_id': '3', 'lat': 1, 'lng': 1},
    ])
    calculate.edges_col.insert_many([
        {'from': '1', 'to': '2', 'weight': 1},
        {'from': '2', 'to': '3', 'weight': 1},
        {'from': '1', 'to': '3', 'weight': 5},
    ])

    route = calculate.find_route('1', '3')
    assert route == [[0, 0], [0, 1], [1, 1]]
