import os
import json
import datetime

import pytz
import asyncio
import requests
from urllib.parse import urljoin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

headers = {
    "Content-Type": "application/json",
    "x-api-key": os.getenv("ASTROLOGY_API_KEY", None),
}


def create_payload(
    year: int,
    month: int,
    day: int,
    hours: int,
    minutes: int,
    seconds: int,
    latitude: float,
    longitude: float,
    timezone: float,
    observation_point: str = "geocentric",
):
    payload = {
        "year": year,
        "month": month,
        "date": day,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "config": {"observation_point": observation_point, "ayanamsha": "lahiri"},
    }
    return payload


class AstrologyApi:
    def __init__(self):
        path = os.path.join(STATIC_DIR, "cities.json")
        fp = open(path)
        self.__cities = json.load(fp)
        self.__all_cities = self.__cities.keys()
        # self.api_key = os.getenv("ASTROLOGY_API_KEY", None)
        self.__api_base_url = os.getenv("ASTROLOGY_API_URL_BASE", None)

    async def get_panchanga(self, place: tuple, lookup_date: datetime):
        params = [
            "nakshatra-durations",
            "tithi-durations",
            "yoga-durations",
            "karana-durations",
        ]

        combined_results = {}
        for api in params:
            resp = await self.__call_panchang_api(place, lookup_date, api)
            combined_results.update(resp)

        # tasks = [self.__call_panchang_api(place, lookup_date, param) for param in params]
        #
        # # Run all tasks concurrently and wait for them to complete
        # results = await asyncio.gather(*tasks)
        #
        # # Combine results into a single dictionary
        # for result in results:
        #     if result:
        #         combined_results.update(result)

        # Print the combined result
        print(combined_results)
        return combined_results

    async def get_navamsa_chart_info(self, place: tuple, lookup_date: datetime):
        resp = await self.__call_panchang_api(place, lookup_date, "navamsa-chart-info")
        return resp

    async def __call_panchang_api(
        self, place: tuple, lookup_date: datetime, api: str
    ) -> dict:
        await asyncio.sleep(0.5)
        lat, lon, tz = place
        payload = json.dumps(
            create_payload(
                lookup_date.year,
                lookup_date.month,
                lookup_date.day,
                lookup_date.hour,
                lookup_date.minute,
                lookup_date.second,
                lat,
                lon,
                tz,
            )
        )
        url = urljoin(self.__api_base_url, api)
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            resp_text = json.loads(response.text)
            if type(resp_text["output"]) is str:
                result = {api: json.loads(resp_text["output"])}
            else:
                result = {api: resp_text["output"]}
            # thithi_result = resp_text["output"]
            print(result)
            return result
        else:
            return {api: {}}
