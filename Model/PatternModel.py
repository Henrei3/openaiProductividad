import os.path

from Model.jsonCreator import JsonFileCreator
from Model.pathFinder import JSONFinder


class PatternModel:

    def __init__(self):
        self.path = "../analysed_records/patterns/word_frequence.json"

    def set_pattern(self, pattern):
        if not os.path.exists("../analysed_records/patterns"):
            os.makedirs("../analysed_records/patterns")
        JsonFileCreator.write(pattern, self.path)

    def get_pattern(self):
        jsonfinder = JSONFinder("../")
        if jsonfinder.find("word_frequence") == -1:
            JsonFileCreator.write(
                {}, self.path
            )
        return jsonfinder.find("word_frequence")

