from fastapi import APIRouter, HTTPException
from app.models.request_models import CityRequest
from app.core.panchanga import Panchanga

router = APIRouter()
panchanga = Panchanga()


@router.post("/")
async def get_navamsa_by_city(city_request: CityRequest):
    city = city_request.city
    lookup_date = city_request.lookup_date
    resp = await panchanga.calculate_navamsa_chart_info(city, lookup_date)
    return resp

