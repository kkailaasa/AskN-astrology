# Panchanga Calculation API

This FastAPI project provides endpoints to calculate Panchanga details for a specific date based on city name, or geographic coordinates and time zone. 

## Setup

### Prerequisites

- Python 3.12.2
- pip (Python package installer)
- Virtual environment (created by PyCharm or manually)

### Installation

1. Clone the repository:

Not set yet

    ```sh
    git clone <repository_url>
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

#### From Command Line

1. Ensure the virtual environment is activated:

    ```sh
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```
2. Default Application port is 8000. Set environment variable `APP_PORT` to change it.


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
  'http://127.0.0.1:8000/panchanga_by_city/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
 "city": "agra",
  "lookup_date": {
    "date": "27/09/1982",
    "hour": "00",
    "minute": "00",
    "second": "00"
  }
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
  "lookup_date": "27/09/1983"
}'
```

### Sample Response

```
{
  "tithi": "Kṛṣṇa pakṣa pañcamī",
  "tithi_time": "15:45:39",
  "nakshatra": "Kṛttikā",
  "nakshatra_time": "15:33:51",
  "yoga": "Pūrṇimā",
  "yoga_time": "15:23:41",
  "karana": "Taitila",
  "vaara": "Maṅgalavāra",
  "rtu": "Varṣā",
  "masa": "Bhādrapada",
  "kali_day": 1857139,
  "salivahana_saka": 1905,
  "gatakali": 5084,
  "samvatsara": "Rudhirodgārī",
  "sunrise": "06:09:13",
  "sunset": "18:08:40",
  "day_duration": "11:59:27"
}
```