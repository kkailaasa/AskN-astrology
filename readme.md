# Panchanga and Navamsa Calculation API

This FastAPI project provides endpoints to calculate Panchanga and Navamsa details for a specific date based on city name, or geographic coordinates and time zone.

This version uses [Free Astrology API](https://freeastrologyapi.com) to get panchanga for a given location and date time except vaar.

This implementation also contains elements of [Drik Panchanga](https://github.com/webresh/drik-panchanga) calculation which works 
correctly for calculating vaara. We are also using the logic to get lat, lng and tz attributes for a given city using city.json 
from the same implementation. Those value are then passed to Astrology API to calculate Tithi, Nakshatra, Karna and Yoga.

This project also contains Dify DSL to calculate Panchanga and Navamsa Chart.



## Setup

### Prerequisites

- Python 3.12.2
- pip (Python package installer)
- Virtual environment (created by PyCharm or manually)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/kkailaasa/AskN-astrology.git
    cd <repository_directory>
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

#### From Container

Docker Compose: 
1. Add API key value to [docker-compose.yml](docker-compose.yml).
2. Navigate to nu_astrology_api and to execute `docker compose up`.

Dockerfile:
1. Add below mentioned api environment variables to docker file before line #15
2. Build docker image `docker build -t astro_api:latest .`
3. `docker run -e APP_PORT=8000 -p 8000:8000 astro_api:latest  `

   ```sh
   ENV ASTROLOGY_API_KEY=<REPLACE WITH API KEY>
   ENV ASTROLOGY_API_URL_BASE=https://json.apiastro.com
   ```

#### From Command Line

1. Ensure the virtual environment is activated:

    ```sh
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```
2. Setup environment variables
   1. Default Application port is 8000. Set environment variable `APP_PORT` to change it.
   2. Setup Panchang API specific environment variables 
      1. ASTROLOGY_API_URL_BASE=https://json.apiastro.com
      2. ASTROLOGY_API_KEY (New key can be obtained from https://freeastrologyapi.com/signup.php)

3. Run the application using `uvicorn` already setup in run.py:

    ```sh
   # navigate in the app folder
    cd nu_astrology_api
   pyhton run.py
    ```

#### From PyCharm

1. Open the project in PyCharm.
2. Ensure the virtual environment is selected in PyCharm:
    - Go to `File` > `Settings` (or `PyCharm` > `Preferences` on macOS).
    - Navigate to `Project: <project_name>` > `Python Interpreter`.
    - Select `.venv` as the interpreter.
3. Create a new run configuration:
    - Go to `Run` > `Edit Configurations`.
    - Click the `+` button and select `Python`.
    - Name the configuration (e.g., "Run/Debug").
    - Set `script` to `run.py`.
    - Ensure the Python interpreter is set to `.venv`.
    
4. Run the application:
    - Select the newly created run configuration and click the Run button.

### Accessing the API Documentation

Once the server is running, you can access the API documentation provided by FastAPI Swagger UI at:

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - Swagger UI
- [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) - ReDoc
- [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json) - OpenAPI JSON

## API Endpoints

### Panchanga by City

- **URL**: `/panchanga_by_city/`
- **Method**: `GET`
- **Parameters**:
  - `city`: The name of the city (string).
  - `lookup_date`: The date for which to calculate Panchanga (query parameter in DD/MM/YYYY format).
- **Response**: JSON object with Panchanga details.

### Example

```sh
curl -X 'POST' \
  'http://localhost:8000/navamsa_chart_by_city/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "city": "delhi",
  "lookup_date": "12/07/2024 14:00:00"
}'
```

### Panchanga by Geo Coordinates

- **URL**: `/panchanga_by_geo_coordinate/`
- **Method**: `GET`
- **Parameters**:
  - `city`: The name of the city (string).
  - `lookup_date`: The date for which to calculate Panchanga (query parameter in DD/MM/YYYY format).
- **Response**: JSON object with Panchanga details.

### Example

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/panchanga_by_geo_coordinate/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "latitude": 27.18333,
  "longitude": 78.01667,
  "timezone": "Asia/Kolkata",
  "lookup_date": "12/07/2024 14:00:00"
}'
```

### Sample Panchangam Response

```
{
  "nakshatra-durations": {
    "number": 12,
    "name": "Uttara Phalguni(Uttara)",
    "starts_at": "2024-07-11 13:03:44",
    "ends_at": "2024-07-12 16:08:17",
    "remaining_percentage_at_given_time": 7.88215107349896
  },
  "tithi-durations": {
    "number": 7,
    "name": "Saptami",
    "paksha": "shukla",
    "completes_at": "2024-07-13 15:06:04",
    "left_precentage": 94.56
  },
  "yoga-durations": {
    "1": {
      "number": 19,
      "name": "Parigha",
      "completion": "2024-07-13 05:13:24",
      "yoga_left_percentage": 60.656713814751484
    },
    "2": {
      "number": 20,
      "name": "Shiva",
      "completion": "2024-07-14 06:14:10"
    }
  },
  "karana-durations": {
    "1": {
      "number": 13,
      "name": "Garija",
      "karana_left_percentage": 89.12797407165928,
      "completion": "2024-07-13 01:50:16"
    },
    "2": {
      "number": 14,
      "name": "Vanija",
      "completion": "2024-07-13 15:06:07"
    },
    "3": {
      "number": 15,
      "name": "Vishti",
      "completion": "2024-07-14 04:18:52"
    }
  },
  "vara": "Śukravāra"
}
```

### Navamsa Chart by City

### Example

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/navamsa_chart_by_city/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "city": "Delhi",
  "lookup_date": "1/1/2005 14:30:00"
}'
```

### Sample Navamsa Response
```sh
{
  "navamsa-chart-info": {
    "0": {
      "name": "Ascendant",
      "isRetro": "false",
      "current_sign": 10
    },
    "1": {
      "name": "Sun",
      "isRetro": "false",
      "current_sign": 6
    },
    "2": {
      "name": "Moon",
      "isRetro": "false",
      "current_sign": 6
    },
    "3": {
      "name": "Mars",
      "isRetro": "false",
      "current_sign": 7
    },
    "4": {
      "name": "Mercury",
      "isRetro": "false",
      "current_sign": 11
    },
    "5": {
      "name": "Jupiter",
      "isRetro": "false",
      "current_sign": 5
    },
    "6": {
      "name": "Venus",
      "isRetro": "false",
      "current_sign": 11
    },
    "7": {
      "name": "Saturn",
      "isRetro": "true",
      "current_sign": 4
    },
    "8": {
      "name": "Rahu",
      "isRetro": "true",
      "current_sign": 2
    },
    "9": {
      "name": "Ketu",
      "isRetro": "true",
      "current_sign": 8
    },
    "10": {
      "name": "Uranus",
      "isRetro": "false",
      "current_sign": 10
    },
    "11": {
      "name": "Neptune",
      "isRetro": "false",
      "current_sign": 3
    },
    "12": {
      "name": "Pluto",
      "isRetro": "false",
      "current_sign": 12
    }
  }
}
```