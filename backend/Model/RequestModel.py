from backend.Model.RecordingModel import RecordingModel
from backend.Model.jsonCreator import JsonFileCreator
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.analyser import SpeechRefinement
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
        if json != -1:
            openai_refinedtext = SpeechRefinement.refine_speech_textOpenAI(json["text"])
            return SpeechRefinement.get_only_agent(openai_refinedtext)
        return json
    def set_response(self, response):
        if not os.path.exists("../analysed_records/audio_text"):
            os.makedirs("../analysed_records/audio_text")
        JsonFileCreator.write(
            {"text": response},
            self.json_path
        )


class ChatGPTRequestModel(RecordingModel):
    nbResponses = 0

    def __init__(self, system, raw_message, name):
        self.nbResponses += 1
        RecordingModel.__init__(self, name)
        self.system = system
        self.message = self.set_raw_message(raw_message)
        self.response: str
        self.json_path = f"../analysed_records/gptAnswer/{name}-{self.nbResponses}GPT.json"

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
        return jsonfinder.find(self.get_name()+"-"+str(self.nbResponses)+"GPT")
