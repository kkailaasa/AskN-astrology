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