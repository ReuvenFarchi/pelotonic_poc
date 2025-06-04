import osmnx as ox
from pymongo import MongoClient
from shapely.geometry import box

client = MongoClient("mongodb://localhost:27017")
db = client["pelotonic"]
nodes_col = db["nodes"]
edges_col = db["edges"]

def download_and_store_osm(lat1, lng1, lat2, lng2, buffer_meters=5000):
    # Step 1: Create bbox from both points
    north = max(lat1, lat2)
    south = min(lat1, lat2)
    east = max(lng1, lng2)
    west = min(lng1, lng2)

    # Step 2: Buffer it using osmnx utility
    bbox_polygon = box(west, south, east, north)
    buffered_polygon = ox.utils_geo._buffered_bounding_box(bbox_polygon, buffer_meters)

    bounds = buffered_polygon.bounds  # (west, south, east, north)
    west, south, east, north = bounds[0], bounds[1], bounds[2], bounds[3]

    # Step 3: Download and store graph
    G = ox.graph_from_bbox(north=north, south=south, east=east, west=west, network_type='bike')

    node_docs = []
    edge_docs = []

    for node_id, data in G.nodes(data=True):
        lat = data.get("y")
        lng = data.get("x")
        node_docs.append({
            "_id": str(node_id),
            "lat": lat,
            "lng": lng,
            "location": {
                "type": "Point",
                "coordinates": [lng, lat]
            }
        })

    for u, v, data in G.edges(data=True):
        edge_docs.append({
            "from": str(u),
            "to": str(v),
            "weight": data.get("length", 1)
        })

    if node_docs:
        try:
            nodes_col.insert_many(node_docs, ordered=False)
        except Exception:
            pass  # skip duplicates

    if edge_docs:
        try:
            edges_col.insert_many(edge_docs, ordered=False)
        except Exception:
            pass  # skip duplicates
