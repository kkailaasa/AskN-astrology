import os
import json

from time import strptime

import pytz
import datetime

# from panchanga_util import *
import difflib
from app.core.panchanga_util import *
from app.models.request_models import *
from app.models.response_models import PanchangamResponse

from app.core.astrology_api import AstrologyApi

# Define the path to the static folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

format_time = lambda t: "%02d:%02d:%02d" % (t[0], t[1], t[2])


class Panchanga:
    def __init__(self):
        path = os.path.join(STATIC_DIR, "cities.json")
        fp = open(path)
        self.cities = json.load(fp)
        self.all_cities = self.cities.keys()
        # Create index based on lat long for faster processing
        self.lat_long_index = {}
        self.set_lat_long_index()
        fp.close()
        path = os.path.join(STATIC_DIR, "sanskrit_names.json")
        fp = open(path, encoding="utf-8")
        sktnames = json.load(fp)
        fp.close()

        self.tithis = sktnames["tithis"]
        self.nakshatras = sktnames["nakshatras"]
        self.vaaras = sktnames["varas"]
        self.yogas = sktnames["yogas"]
        self.karanas = sktnames["karanas"]
        self.masas = sktnames["masas"]
        self.samvats = sktnames["samvats"]
        self.ritus = sktnames["ritus"]

    def set_lat_long_index(self):
        for city, coords in self.cities.items():
            key = (coords["latitude"], coords["longitude"])
            if key not in self.lat_long_index:
                self.lat_long_index[key] = []
            self.lat_long_index[key].append(city)

    def get_cities_by_coordinates(self, lat, long):
        key = (lat, long)
        return self.lat_long_index.get(key, [])

    async def calculate_panchanga_geo(
        self, latitude: float, longitude: float, time_zone: str, lookup_date: str
    ):
        tzone = pytz.timezone(time_zone)
        lookup_date_input = parse_date(lookup_date)
        tz_offset = compute_timezone_offset(lookup_date_input, tzone)
        place = Place(latitude, longitude, tz_offset)
        return await self.__calculate_panchanga(place, lookup_date)

    async def calculate_navamsa_chart_info(self, lookup_city: str, lookup_date: str):
        place, tzone = self.__search_location(lookup_city, lookup_date)
        lookup_date_input = parse_date(lookup_date)
        if place:
            astro = AstrologyApi()
            resp = await astro.get_navamsa_chart_info(place, lookup_date_input)
            return resp

    async def calculate_panchanga_city(self, lookup_city: str, lookup_date: str):
        place, tzone = self.__search_location(lookup_city, lookup_date)
        lookup_date_input = parse_date(lookup_date)
        if place:
            astro = AstrologyApi()
            resp = await astro.get_panchanga(place, lookup_date_input)
            # Add Vara
            vara_masa_samvat = await self.__get_vara_masa_samvat(lookup_date_input, place)
            resp["vara"] = vara_masa_samvat[0]
            resp["masa"] = vara_masa_samvat[1]
            resp["samvat"] = vara_masa_samvat[2]
            resp["rtu"] = vara_masa_samvat[3]
            resp["ayana"] = determine_solstice(lookup_date_input)
            # Add user input to response
            resp["geo_location"] = {
                "city": lookup_city,
                "latitude": place[0],
                "longitude": place[1],
                "timezone": str(tzone),
            }
            return resp

    async def __get_vara_masa_samvat(self, lookup_date: datetime, place: tuple) -> tuple:
        lookup_without_time = datetime(
            lookup_date.year, lookup_date.month, lookup_date.day
        )
        jd_without_time = gregorian_to_jd(lookup_without_time)
        vara = vaara(jd_without_time)
        mas = masa(jd_without_time, place)
        samvat = samvatsara(jd_without_time, mas[0])
        rtu = ritu(mas[0])
        month_name = self.masas[str(mas[0])]
        is_leap = mas[1]
        if is_leap:
            month_name = "Adhika " + month_name.lower()
        p_vara = self.vaaras[str(vara)]
        p_masa = month_name
        p_samvatsara = self.samvats[str(samvat)]
        p_rtu = self.ritus[str(rtu)]
        vara_masa_samvat = (p_vara, p_masa, p_samvatsara, p_rtu)
        return vara_masa_samvat


    async def __calculate_panchanga(
        self, place: tuple, lookup_date: str, tzone: pytz.timezone
    ):
        # tt = {"date": lookup_date.date}
        # lookup_date_no_time = DateTimeRequest(**tt)
        lookup_date_input = parse_date(lookup_date)
        lookup_without_time = datetime(
            lookup_date_input.year, lookup_date_input.month, lookup_date_input.day
        )
        jd_without_time = gregorian_to_jd(lookup_without_time)

        lookup_date_utc = adjust_lookup_dt_to_utc(lookup_date_input, tzone)
        jd_with_time = gregorian_to_jd(lookup_date_input)

        print(f"DateTime Input {lookup_date_input}, without time {lookup_without_time}")

        print(f"JD with time {jd_with_time}, without time {jd_without_time}")
        if place:
            srise = sunrise(jd_without_time, place)[1]
            sset = sunset(jd_without_time, place)[1]
            ti = tithi(jd_with_time, place, jd_without_time)  # not go with the sun
            nak = nakshatra(jd_with_time, place, jd_without_time)  # not go with the sun
            yog = yoga(jd_with_time, place, jd_without_time)
            mas = masa(jd_without_time, place)
            rtu = ritu(mas[0])

            kar = karana(jd_with_time, place)
            vara = vaara(jd_without_time)

            kday = ahargana(jd_without_time)
            kyear, sakayr = elapsed_year(jd_without_time, mas[0])
            samvat = samvatsara(jd_without_time, mas[0])
            day_dur = day_duration(jd_without_time, place)[1]

            p_karana = self.karanas[str(kar[0])]
            p_vaara = self.vaaras[str(vara)]
            p_sunrise = format_time(srise)
            p_sunset = format_time(sset)
            p_salivahana_saka = sakayr
            p_gatakali = kyear
            p_kali_day = kday
            p_rtu = self.ritus[str(rtu)]
            p_samvatsara = self.samvats[str(samvat)]
            p_day_duration = format_time(day_dur)

            # Next update the complex ones
            month_name = self.masas[str(mas[0])]
            is_leap = mas[1]
            if is_leap:
                month_name = "Adhika " + month_name.lower()
            p_masa = month_name

            p_tithi, p_tithi_time = format_name_hms(ti, self.tithis)
            p_yoga, p_yoga_time = format_name_hms(yog, self.yogas)
            p_nakshatra, p_nakshatra_time = format_name_hms(nak, self.nakshatras)

            data = {
                "tithi": p_tithi,
                "tithi_time": p_tithi_time,
                "nakshatra": p_nakshatra,
                "nakshatra_time": p_nakshatra_time,
                "yoga": p_yoga,
                "yoga_time": p_yoga_time,
                "karana": p_karana,
                "vaara": p_vaara,
                "rtu": p_rtu,
                "masa": p_masa,
                "kali_day": p_kali_day,
                "salivahana_saka": p_salivahana_saka,
                "gatakali": p_gatakali,
                "samvatsara": p_samvatsara,
                "sunrise": p_sunrise,
                "sunset": p_sunset,
                "day_duration": p_day_duration,
            }

            panchangam = PanchangamResponse(**data)
            return panchangam

    def __search_location(self, lookup_city, lookup_date):
        city = lookup_city.title()  # Convert to title-case
        if city in self.cities:
            city = self.cities[city]
            lat = city["latitude"]
            lon = city["longitude"]
            tzname = city["timezone"]
            tzone = pytz.timezone(tzname)
            tz_offset = compute_timezone_offset(lookup_date, tzone)
            place = Place(lat, lon, tz_offset)
            return place, tzone
        else:
            # Find nearest match
            nearest = difflib.get_close_matches(city, self.all_cities, 5)
            all_matches = ""
            for m in nearest:
                all_matches += m + "\n"
            msg = (
                city
                + " not found!\n\n"
                + "Did you mean any of these?\n\n"
                + all_matches
            )
            print(msg)
            return None


def compute_timezone_offset(lookup_date, tzone):
    p_date = parse_date(lookup_date)
    p_timezone = tzone
    dt = datetime(p_date.year, p_date.month, p_date.day)
    # offset from UTC (in hours). Needed especially for DST countries
    tz_offset = p_timezone.utcoffset(dt, is_dst=True).total_seconds() / 3600.0
    return tz_offset


def format_name_hms(nhms, lookup):
    name_txt = lookup[str(nhms[0])]
    time_txt = format_time(nhms[1])
    if len(nhms) == 4:
        name_txt += "\n" + lookup[str(nhms[2])]
        time_txt += "\n" + format_time(nhms[3])

    return name_txt, time_txt


def parse_date(lookup_date: str):
    try:
        # date_str = f"{lookup_date.date} {lookup_date.hour}:{lookup_date.minute}:{lookup_date.second}"
        # dt = strptime(date_str, "%d/%m/%Y")
        # Date(dt.tm_year, dt.tm_mon, dt.tm_mday)
        lookup_date = datetime.strptime(lookup_date, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        # Probably the user entered negative year, strptime can't handle it.
        day, month, year = map(int, lookup_date.split("/"))
        lookup_date = Date(year, month, day)
    return lookup_date


def adjust_lookup_dt_to_utc(local_datetime: datetime, time_zone: pytz.timezone):
    # datetime_str = "27/09/1982 5:30:00"
    # Replace 'US/Eastern' with your actual local timezone if known
    # local_timezone = timezone('US/Eastern')

    # Parse the string with local timezone information
    # dt = datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
    dt_with_local_tz = local_datetime.replace(tzinfo=time_zone)

    # Convert to UTC from the local timezone
    # tt = dt_with_local_tz.astimezone(pytz.utc)
    dt_utc = dt_with_local_tz.astimezone(pytz.utc)

    print(f"User input converted to UTC {dt_utc}")
    return dt_utc


def determine_solstice(lookup_date):
    """
    Determine whether the given date falls within Uttarayana or Dakshinayana.

    Args:
    date (datetime): The date to check.

    Returns:
    str: "Uttarayana" if the date is within Uttarayana, "Dakshinayana" if the date is within Dakshinayana.
    """
    year = lookup_date.year

    # Define the start and end dates for Uttarayana and Dakshinayana for the given year
    uttarayana_start = datetime(year, 1, 14)
    uttarayana_end = datetime(year, 7, 14)

    # Determine the solstice period for the given date
    if uttarayana_start <= lookup_date < uttarayana_end:
        return "Uttarayana"
    else:
        return "Dakshinayana"