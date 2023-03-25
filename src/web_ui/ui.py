from kafka import KafkaConsumer
from datetime import datetime, timedelta
from typing import Tuple
import streamlit as st
from src.sensors import SENSORS_LIST

st.set_page_config(layout="wide")


def intro() -> None:
    st.write("# Welcome to the sensors UI! 👋")
    st.markdown(
        """
        In this page you can retrieve information about a single sensor or a family of sensors and view some statistics 
        about them.
        """
    )
    return


def get_query_values() -> Tuple[str, datetime, datetime]:
    current_datetime: datetime = datetime.now()
    default_start_time: datetime = current_datetime - timedelta(days=7)
    sensor: str = st.selectbox(label='sensors', options=['a', 'b'])
    start_date = st.date_input("Set starting date", value=default_start_time)
    end_date = st.date_input("Set end date", value=current_datetime)
    return sensor, start_date, end_date


def main() -> None:
    intro()
    sensor_name, start_date, end_date = get_query_values()
    st.write(sensor_name)
    st.write(start_date)
    st.write(end_date)
    return


if __name__ == '__main__':
    sensors = [s() for s in SENSORS_LIST]

    main()
