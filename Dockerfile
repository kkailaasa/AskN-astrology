FROM python:3.12-slim

# Install build-essential and gcc for pyswisseph
RUN apt-get update && \
    apt-get install -y build-essential gcc && \
    apt-get clean

WORKDIR /api

COPY . /api/

RUN  pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $APP_PORT

# Command to run the application
CMD ["python", "run.py"]
