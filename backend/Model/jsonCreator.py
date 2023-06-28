import json
import os


class JsonFileCreator:
    @staticmethod
    def write(obj, file_path):
        """ This method will write an object in the form of a json object
         in the specified file_path.
         File path must have the file name in its path"""
        json_object = json.dumps(obj)
        with open(file_path, "w") as file:
            file.write(json_object)

    @staticmethod
    def write_message(message, path):
        message = {"text": message}
        JsonFileCreator.write(message, path)
