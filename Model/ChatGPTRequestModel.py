import RecordingModel
from jsonCreator import JsonFileCreator
from pathFinder import JSONFinder
import os


class ChatGPTRequestModel(RecordingModel):
    def __init__(self, system, raw_message, name):
        super.__init__(name)
        self.system = system
        self.message = [
            {"role": "system", "content": system},
            {"role": "user", "content": raw_message}
        ]
        self.response = ""
        self.json_path = "../analysed_records/gptAnswer/"+name+"GPT.json"

    def get_system(self):
        return self.system

    def set_system(self, system):
        self.system = system

    def get_message(self):
        return self.message

    def set_raw_message(self, raw_message):
        self.message = [
            {"role": "system", "content": self.system},
            {"role": "user", "content": raw_message}
        ]

    def set_response(self, response):
        if not os.path.exists("../analysed_records/gptAnswer"):
            os.makedirs("../analysed_records/gptAnswer")
        JsonFileCreator.write_message(response, self.json_path)

    def get_response(self):
        jsonfinder = JSONFinder("../")
        return jsonfinder.find(self.get_name()+"GPT")
