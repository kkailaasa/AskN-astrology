from fastapi import FastAPI
from app.api.endpoints import (
    panchanga_by_city,
    panchanga_by_location,
    navamsa_chart_by_city,
)

app = FastAPI()

app.include_router(
    panchanga_by_city.router, prefix="/panchanga_by_city", tags=["by_city"]
)
app.include_router(
    panchanga_by_location.router,
    prefix="/panchanga_by_geo_coordinate",
    tags=["by_geo_coordinate"],
)
app.include_router(
    navamsa_chart_by_city.router, prefix="/navamsa_chart_by_city", tags=["by_city"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
