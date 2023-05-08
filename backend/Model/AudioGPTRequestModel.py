from backend.Model.RecordingModel import RecordingModel
from backend.Model.jsonCreator import JsonFileCreator
from backend.Model.pathFinder import JSONFinder
from backend.Controller.analyser import SpeechRefinement
import os


class AudioGPTRequestModel(RecordingModel):

    def __init__(self, prompt, audio_path, name):
        self.prompt = prompt
        self.audioName = audio_path
        self.json_path = "../analysed_records/audio_text/" + name + ".json"
        self.response = {}
        RecordingModel.__init__(self, name)

    def __str__(self):
        return f"Prompt : {self.get_prompt()} Audio_Path : {self.get_audio_path()}"


    def get_prompt(self):
        return self.prompt

    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_audio_path(self):
        return self.audioName

    def set_audio_path(self, audio_name):
        self.audioName = audio_name

    def get_response(self):
        json_finder = JSONFinder("../")
        json = json_finder.find(self.name)
        return SpeechRefinement.refine_speech_textOpenAI(json["text"])

    def set_response(self, response):
        if not os.path.exists("../analysed_records/audio_text"):
            os.makedirs("../analysed_records/audio_text")
        JsonFileCreator.write(
            {"text": response},
            self.json_path
        )
