from pydantic import BaseModel


class PanchangamResponse(BaseModel):
    tithi: str
    tithi_time: str
    nakshatra: str
    nakshatra_time: str
    yoga: str
    yoga_time: str
    karana: str
    vaara: str
    rtu: str
    masa: str
    kali_day: float
    salivahana_saka: int
    gatakali: int
    samvatsara: str
    sunrise: str
    sunset: str
    day_duration: str

