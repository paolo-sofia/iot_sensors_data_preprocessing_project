from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
from src.spark_streaming.data_readings import compute_data_statistics


class SensorData(BaseModel):
    sensor_name: str
    sensor_type: str
    start_datetime: datetime
    end_datetime: datetime


app = FastAPI()


@app.post('sensor_data')
def get_data(inputs: SensorData):
    return compute_data_statistics(inputs.sensor_name, inputs.sensor_type, inputs.start_datetime, inputs.end_datetime)
