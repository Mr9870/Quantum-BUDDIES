from fastapi import FastAPI
from pydantic import BaseModel
from geopy.distance import geodesic

app = FastAPI()

class LocationData(BaseModel):
    latitude: float
    longitude: float
    speed: float

# Store previous location for distance calculation
previous_location = None
total_distance = 0.0

@app.post("/track-location/")
async def track_location(data: LocationData):
    global previous_location, total_distance

    # If it's the first location, just store it
    if previous_location is None:
        previous_location = (data.latitude, data.longitude)
        return {"message": "Tracking started", "distance_km": total_distance, "speed_kmh": data.speed * 3.6}

    # Calculate distance from last location
    current_location = (data.latitude, data.longitude)
    distance = geodesic(previous_location, current_location).km
    total_distance += distance
    previous_location = current_location

    return {"distance_km": total_distance, "speed_kmh": data.speed * 3.6}

# Run the server: uvicorn app:app --reload