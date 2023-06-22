import json
import os


class JsonFileCreator:
    @staticmethod
    def write(diction, path):
        json_object = json.dumps(diction)
        with open(path, "w") as file:
            file.write(json_object)

    @staticmethod
    def write_message(message, path):
        message = {"text": message}
        JsonFileCreator.write(message, path)
