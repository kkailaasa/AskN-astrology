from fastapi import APIRouter, HTTPException
from app.models.request_models import CityRequest
from app.core.panchanga import Panchanga

router = APIRouter()
panchanga = Panchanga()


@router.post("/")
async def get_panchanga_by_city(city_request: CityRequest):
    city = city_request.city
    lookup_date = city_request.lookup_date
    resp = await panchanga.calculate_panchanga_city(city, lookup_date)
    return resp

