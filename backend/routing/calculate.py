from pymongo import MongoClient
import heapq

client = MongoClient("mongodb://localhost:27017")
db = client["pelotonic"]
nodes_col = db["nodes"]
edges_col = db["edges"]

def build_graph():
    graph = {}

    for edge in edges_col.find():
        u = edge["from"]
        v = edge["to"]
        w = edge["weight"]
        graph.setdefault(u, []).append((v, w))

    return graph

def get_node_coords(node_id):
    doc = nodes_col.find_one({"_id": node_id})
    if doc:
        return [doc["lat"], doc["lng"]]
    return None

def find_route(start_id, end_id):
    graph = build_graph()
    queue = [(0, start_id, [])]
    visited = set()

    while queue:
        cost, current, path = heapq.heappop(queue)

        if current in visited:
            continue
        visited.add(current)

        path = path + [current]

        if current == end_id:
            return [get_node_coords(n) for n in path if get_node_coords(n)]

        for neighbor, weight in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return []
