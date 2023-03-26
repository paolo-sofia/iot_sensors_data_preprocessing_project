import importlib
import inspect
import os
import sys
from pathlib import Path
from typing import Generator, List, Optional

from app.sensors_producers.sensors.abstract_sensor import AbstractSensor

SENSORS_LIST: List[str] = []


def get_module_name(module_name: str) -> Optional[str]:
    """
    This is a helper function that checks if the given module name has been imported or not, if so, returns the name of
    the module, else None. It uses the sys.modules dictionary to check if the module has been imported
    :param module_name: the module name to check
    :return: the sys.modules key of the model if it has been imported, None otherwise
    """
    for k in sys.modules.keys():
        if module_name in k:
            return k
    return None


def get_all_sensors_object(package_name: str, base_dir: str) -> None:
    """
    Helper function used for getting the list of sensors. It lists all the submodules inside the given base_dir
    directory, imports the submodule and then from it retrieves only the sensors objects and add each sensor to the
    sensors_list
    :param package_name: the package name used for performing the relative import for the submodule
    :param base_dir: the base dir where to get all the submodules
    :param sensors_list: the list where all the found checkers will be added
    :return: None
    """
    global SENSORS_LIST
    modules: Generator[str] = Path(base_dir).glob('*.py')

    for module in modules:
        importlib.import_module(f'.{module.stem}', package=package_name)
        for name, cls in inspect.getmembers(sys.modules[get_module_name(module.stem)], inspect.isclass):
            if issubclass(cls, AbstractSensor) and cls != AbstractSensor:
                SENSORS_LIST.append(cls)
    return


get_all_sensors_object(__package__, os.path.dirname(__file__))
