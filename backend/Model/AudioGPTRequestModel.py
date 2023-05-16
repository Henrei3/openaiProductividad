from backend.Model.RecordingModel import RecordingModel
from backend.Model.jsonCreator import JsonFileCreator
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.analyser import SpeechRefinement
import os


class AudioGPTRequestModel(RecordingModel):

    def __init__(self, prompt, audio_path, name):
        RecordingModel.__init__(self, name)
        self.prompt = prompt
        self.audioPath = audio_path
        self.json_path = f"../analysed_records/audio_text/{name}.json"
        self.response = {}

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

    def get_response(self):
        json_finder = JSONFinder("../analysed_records/audio_text/")
        json = json_finder.find(self.name)
        return SpeechRefinement.refine_speech_textOpenAI(json["text"])

    def set_response(self, response):
        if not os.path.exists("../analysed_records/audio_text"):
            os.makedirs("../analysed_records/audio_text")
        JsonFileCreator.write(
            {"text": response},
            self.json_path
        )
