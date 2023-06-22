import openai
from decouple import config
from backend.Model.RequestModel import ChatGPTRequestModel, AudioGPTRequestModel,OpenAIModelInterface
import abc
from typing import Union


class OpenAiRequestInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'execute_request') and
                callable(subclass.execute_request))


class OpenAIAudioRequest:

    @staticmethod
    def execute_request(gpt_request: AudioGPTRequestModel):
        APIKEY = config('whisper')

        audio = gpt_request.get_audio_path()
        with open(audio, "rb") as audio_file:
            response = openai.Audio.transcribe(
                api_key=APIKEY,
                model="whisper-1",
                file=audio_file,
                prompt=gpt_request.get_prompt()
            )
            print(response)
        return response["text"]


class OpenAIChatRequest:

    @staticmethod
    def execute_request(gpt_model: ChatGPTRequestModel):

        APIKEY = config('whisper')
        messages = gpt_model.get_message()

        response = openai.ChatCompletion.create(
            api_key=APIKEY,
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=2000,
            messages=messages
        )

        print(response)
        return response['choices'][0]['message']['content']
    @staticmethod
    def message_parser(raw_message, system):
        message = [
            {"role": "system", "content": system},
            {"role": "user", "content": raw_message}
        ]
        return message


class OpenAIProxy:
    openai_model: OpenAIModelInterface

    def __init__(self, openai_model: OpenAIModelInterface):
        self.openai_model = openai_model

    @classmethod
    def check_access(cls, openai_model: OpenAIModelInterface):
        response: Union[dict, int] = openai_model.get_response()
        if response == -1:
            audio_response = cls._operation(openai_model)
            openai_model.set_response(audio_response)
            return openai_model.get_response()
        else:
            return response

    @staticmethod
    def _operation(openai_model):
        if type(openai_model) is AudioGPTRequestModel:
            audiogpt_request_model: AudioGPTRequestModel = openai_model
            return OpenAIAudioRequest.execute_request(audiogpt_request_model)
        elif type(openai_model) is ChatGPTRequestModel:
            chatgpt_request_model: ChatGPTRequestModel = openai_model
            return OpenAIChatRequest.execute_request(chatgpt_request_model)














