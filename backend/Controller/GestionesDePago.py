from backend.Controller.pathFinder import WavFinder
from backend.Model.RequestModel import AudioGPTRequestModel
from backend.Model.RequestModel import ChatGPTRequestModel
from backend.Controller.GPTCreator import OpenAIAudioRequest
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.analyser import PatternController
from decouple import config
import os


def gestiones_de_pago():
    prompt = config('PROMPT')
    wavfinder = WavFinder("./")

    if not os.path.exists("./analysed_records"):
        os.makedirs("./analysed_records")
        os.makedirs("./analysed_records/audio_text")
        os.makedirs("./analysed_records/gptAnswer")
        os.makedirs("./analysed_records/patterns")

    wavs = wavfinder.find_all()
    for audio_file in wavs:
        """ Speech To Text """
        audio_gpt = AudioGPTRequestModel(prompt, audio_file[1], audio_file[0])
        audio_response = OpenAIAudioRequest.execute_request(audio_gpt)
        audio_gpt.set_response(audio_response)

        """ text IA text """
        outjson = audio_gpt.get_response()
        refined_speech = SpeechRefinement.refine_speech_textOpenAI(outjson["text"])
        system = "Vas a leer una llamada de un agente de cobranzas exitosa. Dame los patrones que permitieron que eso sea posible. Ten en cuenta que la llamada fue traducida por whisper-1 (speechToText)"
        chat_gpt = ChatGPTRequestModel(system, refined_speech, audio_file[0])
        chat_response = OpenAIAudioRequest.chat_request(chat_gpt)
        chat_gpt.set_response(chat_response)

        """  Patterns """
        PatternController.countWords(audio_file[0])
