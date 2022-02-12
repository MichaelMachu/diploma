from json import dumps, loads, load

class DataProcess:

    def to_json(dictValue: dict) -> str:
        return dumps(dictValue)

    def to_dict(jsonStr: str) -> dict:
        return loads(jsonStr)

    def save_to_json_file(filename: str, jsonStr: str) -> None:
        """filename should also contains a path to the location where the file will be saved"""
        with open("{}.json".format(filename), 'w') as file:
            file.write(json_string)

    def load_from_json_file(filename: str) -> str:
        """filename should also contains a path to the location where the file is saved"""
        data = ""
        with open("{}.json".format(filename)) as file:
            data = load(file)
        return data