from fastapi import FastAPI
from typing import List

from backend.services.nasa_service import fetch_asteroids
from backend.utils.cache import get_cached_data, set_cache
from backend.models.asteroid import Asteroid



app = FastAPI(title="AstroGuard Backend")


@app.get("/asteroids", response_model=List[Asteroid])
def get_asteroids():
    cached = get_cached_data()
    if cached:
        return cached

    data = fetch_asteroids()
    set_cache(data)
    return data
