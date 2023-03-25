from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime


class SensorData(BaseModel):
    sensor_name: str
    sensor_type: str
    start_datetime: datetime
    end_datetime: datetime


app = FastAPI()


@app.post('sensor_data')
def get_data(input: SensorData):
    pass
