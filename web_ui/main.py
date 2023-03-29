import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import pandas as pd
import requests
import streamlit as st
from kafka3 import KafkaConsumer

from src.sensor_type import QueryOptions, SensorFamilyType

st.set_page_config(layout="wide", page_title="IOT Sensors UI")

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

RADIO_OPTION_SENSOR = 'Single sensor'
RADIO_OPTION_SENSOR_FAMILY = 'Family of sensors_producers'
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
AVAILABLE_SENSORS: Dict[str, str] = {}


def intro() -> None:
    """
    Helper function, contains welcome message and little introduction about the ui
    :return:
    """
    st.write("# Welcome to the sensors_producers UI! 👋")
    st.markdown(
        """
        In this page you can retrieve information about a single sensor or a family of sensors_producers and view some 
        statistics about them.
        """
    )
    return


def show_available_sensors_family() -> List[str]:
    """
    Returns the list of available family of sensors
    :return: the list of available family of sensors
    """
    return SensorFamilyType.ALL_TYPES


def get_available_sensors() -> None:
    """Runs a kafka consumer that reads the sensor_topic topic to get all the active sensors, and sets the global
    variable AVAILABLE_SENSOR that contains a dict with the active sensors
    :return None"""
    global AVAILABLE_SENSORS
    consumer: KafkaConsumer = KafkaConsumer('sensors_topic', bootstrap_servers='broker:9092',
                                            auto_offset_reset='earliest', group_id='sensors',
                                            consumer_timeout_ms=100, api_version=(3, 4, 0))
    consumer.poll()
    messages: List[Dict[str, Any]] = [json.loads(msg.value.decode('utf-8')) for msg in consumer]
    AVAILABLE_SENSORS = {msg['id']: msg['name'] for msg in messages}
    return


def show_available_sensors() -> List[str]:
    """
    Returns the active sensors; names to be shown in the select box
    :return: the list of active sensors' names
    """
    return AVAILABLE_SENSORS.keys()


def extract_sensor_name(option: str) -> List[str]:
    try:
        return AVAILABLE_SENSORS[option]
    except Exception as e:
        return option


def display_form_and_get_query_values(sensor_options: List[str], sensor_type: str) -> Dict[str, Union[str, datetime]]:
    current_datetime: datetime = datetime.now()
    min_start_time: datetime = current_datetime - timedelta(days=7)
    default_start_time: datetime = current_datetime - timedelta(hours=1)
    with st.form('data_to_get_form'):
        start_datetime: str = datetime.isoformat(st.slider(
            "Start timeframe",
            min_value=min_start_time,
            max_value=current_datetime,
            value=default_start_time,
            step=(timedelta(minutes=1)),
            format="DD/MM/YY - hh:mm"), timespec='seconds', sep=' ')

        end_datetime: str = datetime.isoformat(st.slider(
            "Start timeframe",
            min_value=min_start_time,
            max_value=current_datetime,
            value=current_datetime,
            step=(timedelta(minutes=1)),
            format="DD/MM/YY - hh:mm"), timespec='seconds', sep=' ')
        label: str = 'Sensors' if sensor_type == QueryOptions.SENSOR else 'Sensor Family'
        selected_sensor: str = st.selectbox(label=label, options=sensor_options,
                                            format_func=extract_sensor_name)

        submitted: bool = st.form_submit_button("Submit", use_container_width=True)
        if submitted:
            return {
                'sensor_name': selected_sensor,
                'sensor_type': sensor_type,
                'start_datetime': start_datetime,
                'end_datetime': end_datetime,
            }
        else:
            return {}


def display_data(dataframe: pd.DataFrame) -> None:
    """Helper function used for displaying the computed data as a table"""
    st.markdown(f'### These are some statistics about the sensor')
    st.dataframe(dataframe, use_container_width=True)
    return


def send_api_request(inputs: Dict[str, Any]) -> pd.DataFrame:
    """
    Sends the api requests with the given inputs and returns the response data formatted as a pandas dataframe. If
    response is an error, returns an empty dataframe
    :param inputs:
    :return:
    """
    response: requests.Response = requests.post(url="http://spark_api:8000/sensor_data/", json=inputs, headers=HEADERS,
                                                verify=False)
    if response.ok:
        st.success("Successfully computed data")
        try:
            return pd.DataFrame().from_dict(response.json())
        except Exception as e:
            logger.error(e)
            return pd.DataFrame()
    else:
        st.error(response.text)
        return pd.DataFrame()


def main() -> None:
    """
    Main loop, it runs the web ui logic
    :return:
    """
    intro()
    option: str = st.radio(label='Which data do you want to get?', options=[RADIO_OPTION_SENSOR,
                                                                            RADIO_OPTION_SENSOR_FAMILY])
    if option == RADIO_OPTION_SENSOR:
        get_available_sensors()
        available_sensors: List[str] = show_available_sensors()
        sensor_type: str = QueryOptions.SENSOR
    else:
        available_sensors: List[str] = SensorFamilyType.ALL_TYPES
        sensor_type: str = QueryOptions.SENSOR_FAMILY

    inputs = display_form_and_get_query_values(available_sensors, sensor_type)
    if not inputs:
        return

    response_df: pd.DataFrame = send_api_request(inputs)
    if not response_df.empty:
        display_data(response_df)

    return


if __name__ == '__main__':
    main()
