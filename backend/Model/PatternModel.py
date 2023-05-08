import os.path

from backend.Model.jsonCreator import JsonFileCreator
from backend.Model.pathFinder import JSONFinder


class PatternModel:

    def __init__(self):
        self.path = "../backend/analysed_records/patterns/word_frequence.json"

    def set_pattern(self, pattern):
        if not os.path.exists("../backend/analysed_records/patterns"):
            os.makedirs("../backend/analysed_records/patterns")
        JsonFileCreator.write(pattern, self.path)

    def get_pattern(self):
        jsonfinder = JSONFinder("../")
        if jsonfinder.find("word_frequence") == -1:
            JsonFileCreator.write(
                {}, self.path
            )
        return jsonfinder.find("word_frequence")

