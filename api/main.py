import logging

from fastapi import FastAPI
from pydantic import BaseModel

from spark_streaming.data_readings import compute_data_statistics, create_session_and_start_stream

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


class SensorData(BaseModel):
    sensor_name: str
    sensor_type: str
    start_datetime: str
    end_datetime: str


app = FastAPI()
create_session_and_start_stream()


@app.post('/sensor_data/')
def get_data(inputs: SensorData):
    return compute_data_statistics(inputs.sensor_name, inputs.sensor_type, inputs.start_datetime, inputs.end_datetime)


@app.get('/health')
def get_data():
    return {'health': 'ok'}
