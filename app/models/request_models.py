from pydantic import BaseModel, confloat, field_validator
from datetime import datetime
import pytz
from pydantic.v1 import validator


class DateTimeRequest(BaseModel):
    date: str
    hour: str = "00"
    minute: str = "00"
    second: str = "00"

    @validator('date')
    def validate_date(self, v):
        try:
            datetime.strptime(v, '%d/%m/%Y')
        except ValueError:
            raise ValueError('Date must be in DD/MM/YYYY format')
        return v


class CityRequest(BaseModel):
    city: str
    lookup_date: str

    @validator('date')
    def validate_date(self, v):
        try:
            datetime.strptime(v, "%d/%m/%Y %H:%M:%S")
        except ValueError:
            raise ValueError('Date must be in DD/MM/YYYY HH:MM:SS format')
        return v


class LocationRequest(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)
    timezone: str
    lookup_date: DateTimeRequest

    @validator('timezone')
    def validate_timezone(self, v):
        if v not in pytz.all_timezones:
            raise ValueError('Invalid timezone')
        return v

