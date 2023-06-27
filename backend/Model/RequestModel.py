from backend.Model.RecordingModel import RecordingModel
from backend.Model.jsonCreator import JsonFileCreator
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.PostGreSQLController import PostgreController
import os
import abc


class OpenAIModelInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_response') and
                callable(subclass.get_response) and
                hasattr(subclass, 'set_response') and
                callable(subclass.set_response))


class AudioGPTRequestModel(RecordingModel):

    def __init__(self, prompt, audio_path, name):
        RecordingModel.__init__(self, name)
        self.prompt = prompt
        self.audioPath = audio_path
        self.json_path = f"../analysed_records/audio_text/{name}.json"

    def __str__(self):
        return f"Prompt : {self.get_prompt()} Audio_Path : {self.get_audio_path()}"

    def get_prompt(self):
        return self.prompt

    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_audio_path(self):
        return self.audioPath

    def set_audio_path(self, audio_path):
        self.audioPath = audio_path

    def set_response(self, response):
        recording_id = self.get_recording_row()[0]
        PostgreController.add_audio_text(recording_id, '{"text":'+response+'}')

    def get_response(self):
        postgre_controller_result = PostgreController.get_audio_text(self.get_recording_row()[0])
        if postgre_controller_result:
            return postgre_controller_result[0]
        return postgre_controller_result


class ChatGPTRequestModel(RecordingModel):

    def __init__(self, system, raw_message, name):
        RecordingModel.__init__(self, name)
        self.system = system
        self.message = self.set_raw_message(raw_message)
        self.json_path = f"../analysed_records/gptAnswer/{name}GPT.json"

    def get_system(self):
        return self.system

    def set_system(self, system):
        self.system = system

    def get_message(self):
        return self.message

    def set_raw_message(self, raw_message):
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": raw_message}
        ]

    def set_response(self, response):
        if not os.path.exists("../analysed_records/gptAnswer"):
            os.makedirs("../analysed_records/gptAnswer")
        JsonFileCreator.write_message(response, self.json_path)

    def get_response(self):
        jsonfinder = JSONFinder("../")
        return jsonfinder.find(self.get_name()+"-GPT")


class EmbeddingRequestModel(RecordingModel):
    def __init__(self, name: str, text: str):
        RecordingModel.__init__(self, name)
        self.text = text

    def get_text(self):
        return self.text

    def set_response(self, embedding: dict):
        recording_id = self.get_recording_row()[0]
        PostgreController.add_embedding(recording_id, embedding)

    def get_response(self):
        postgre_controller_result = PostgreController.get_embedding(self.name)[1]
        if postgre_controller_result:
            return postgre_controller_result[0]
        return postgre_controller_result
