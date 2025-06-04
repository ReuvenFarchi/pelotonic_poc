from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from db.nearest_node import find_nearest_node
from db.store_graph import download_and_store_osm
from routing.calculate import find_route  # You’ll create this later

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/route")
def get_route(origin: str, destination: str):
    origin_lat, origin_lng = map(float, origin.split(","))
    dest_lat, dest_lng = map(float, destination.split(","))

    # Step 1: Find nearest nodes
    origin_node = find_nearest_node(origin_lat, origin_lng)
    dest_node = find_nearest_node(dest_lat, dest_lng)

    # Step 1.1: If missing, fetch OSM and populate DB
    if not origin_node or not dest_node:
        print("Nearest nodes not found — fetching OSM data...")
        download_and_store_osm(origin_lat, origin_lng, dest_lat, dest_lng)

        # Try again
        origin_node = find_nearest_node(origin_lat, origin_lng)
        dest_node = find_nearest_node(dest_lat, dest_lng)

        if not origin_node or not dest_node:
            return {"error": "Could not resolve nearest nodes after loading OSM."}

    # Step 2: Find route (from origin_node to dest_node)
    path = find_route(origin_node[0], dest_node[0])  # You return (_id, lat, lng) in nearest_node

    # Step 3: Format response
    return {
        "routes": [
            {
                "path": [[origin_lat, origin_lng]] + path + [[dest_lat, dest_lng]],  # stitched real start/end
                "distance_km": 5.3,  # placeholder
                "time_min": 20       # placeholder
            }
        ]
    }
