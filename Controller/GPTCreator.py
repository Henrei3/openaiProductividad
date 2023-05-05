import openai
from decouple import config
from Model.AudioGPTRequestModel import AudioGPTRequestModel


class OpenAIRequestCreator:

    @staticmethod
    def audio_request(gpt_request):
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

    @staticmethod
    def chat_request(gptModel):

        APIKEY = config('whisper')
        messages = gptModel.get_message()

        response = openai.ChatCompletion.create(
            api_key=APIKEY,
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=300,
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
