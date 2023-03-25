import json
from kafka import KafkaConsumer
from datetime import datetime, timedelta
from typing import List, Dict, Union
import streamlit as st
import requests
from src.sensors.sensor_type import SensorFamilyType, QueryOptions

st.set_page_config(layout="wide")

RADIO_OPTION_SENSOR = 'Single sensor'
RADIO_OPTION_SENSOR_FAMILY = 'Family of sensors'


def intro() -> None:
    st.write("# Welcome to the sensors UI! 👋")
    st.markdown(
        """
        In this page you can retrieve information about a single sensor or a family of sensors and view some statistics 
        about them.
        """
    )
    return


def show_available_sensors() -> List[str]:
    """Shows the list of all the active sensors (sensors that have sent at least one data through the topic"""
    consumer: KafkaConsumer = KafkaConsumer('sensors_topic', bootstrap_servers='')
    return [msg for msg in consumer]


def show_available_sensors_family() -> List[str]:
    return SensorFamilyType.ALL_TYPES


def display_form_and_get_query_values(sensor_options: List[str], sensor_type: str) -> Dict[str, Union[str, datetime]]:
    current_datetime: datetime = datetime.now()
    min_start_time: datetime = current_datetime - timedelta(days=7)
    default_start_time: datetime = current_datetime - timedelta(hours=1)
    with st.form('data_to_get_form'):
        start_datetime: datetime = st.slider(
            "Start timeframe",
            min_value=min_start_time,
            max_value=current_datetime,
            value=default_start_time,
            step=(timedelta(minutes=1)),
            format="DD/MM/YY - hh:mm")

        end_datetime: datetime = st.slider(
            "Start timeframe",
            min_value=min_start_time,
            max_value=current_datetime,
            value=current_datetime,
            step=(timedelta(minutes=1)),
            format="DD/MM/YY - hh:mm")
        selected_sensor: str = st.selectbox(label='sensors', options=sensor_options)

        submitted: bool = st.form_submit_button("Submit")
        if submitted:
            return {
                'sensor': selected_sensor,
                'sensor_type': sensor_type,
                'start_datetime': start_datetime,
                'end_datetime': end_datetime
            }
        else:
            return {}


def main() -> None:
    intro()
    option: str = st.radio(label='Which data do you want to get?', options=[RADIO_OPTION_SENSOR,
                                                                            RADIO_OPTION_SENSOR_FAMILY])
    sensor_type: str = ''
    if option == RADIO_OPTION_SENSOR:
        available_sensors = show_available_sensors()
        sensor_type = QueryOptions.SENSOR
    else:
        available_sensors = show_available_sensors_family()
        sensor_type = QueryOptions.SENSOR_FAMILY

    inputs = display_form_and_get_query_values(available_sensors, sensor_type)

    response: requests.Response = requests.post(url="http://127.0.0.1:8000/sensor_data", data=json.dumps(inputs))
    return


# if __name__ == '__main__':
main()
