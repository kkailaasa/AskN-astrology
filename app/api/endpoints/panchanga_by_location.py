from fastapi import APIRouter, HTTPException

from app.core.panchanga import Panchanga
from app.models.request_models import LocationRequest

router = APIRouter()
panchanga = Panchanga()


@router.post("/")
async def get_panchanga_by_location(location_request: LocationRequest):
    latitude = location_request.latitude
    longitude = location_request.longitude
    tzone = location_request.timezone
    lookup_date = location_request.lookup_date
    resp = await panchanga.calculate_panchanga_geo(
        latitude, longitude, tzone, lookup_date
    )
    return resp
