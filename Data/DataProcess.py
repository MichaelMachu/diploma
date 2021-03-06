from json import dumps, loads, load
from os import path
from numpy import ndarray

class DataProcess:

    def to_json(dictValue: dict) -> str:
        return dumps(dictValue)

    def to_dict(jsonStr: str) -> dict:
        return loads(jsonStr)

    def to_list(data: ndarray) -> list:
        """Converts ndarray into list, list can be also send if not sure if it is a list or ndarray."""
        return data.tolist() if type(data) == ndarray else data

    def save_to_json_file(filename: str, jsonStr: str) -> None:
        """filename should also contains a path to the location where the file will be saved"""
        with open("{}.json".format(filename), 'w') as file:
            file.write(jsonStr)

    def load_from_json_file(filename: str) -> dict:
        """filename should also contains a path to the location where the file is saved"""
        filename = "{}.json".format(filename)
        if not path.exists(filename):
            return None
        data = ""
        with open(filename) as file:
            data = load(file)
        return data