from pymongo import MongoClient, GEOSPHERE

client = MongoClient("mongodb://localhost:27017")
db = client["pelotonic"]
nodes = db["nodes"]

# Ensure index
nodes.create_index([("location", GEOSPHERE)])

def find_nearest_node(lat, lng):
    point = {
        "type": "Point",
        "coordinates": [lng, lat]
    }

    nearest = nodes.find_one({
        "location": {
            "$near": {
                "$geometry": point
            }
        }
    })

    if not nearest:
        return None

    return (nearest["_id"], nearest["lat"], nearest["lng"])
