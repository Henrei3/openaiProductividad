from backend.Model.RecordingModel import RecordingModel
from backend.Model.AudioGPTRequestModel import AudioGPTRequestModel
from backend.Model.DataBase import SQLSERVERDBModel
from backend.Controller.GPTCreator import OpenAIRequestCreator
from backend.Controller.PhrasesController import EncouragedPhrasesController
from backend.Controller.PhrasesController import ProhibitedPhrasesController
from backend.Model.PhrasesModel import EncouragedPhrasesModel,ProhibitedPhrasesModel
from backend.Model.ChatGPTRequestModel import ChatGPTRequestModel
import subprocess
import time


class QualityAssurance:

    @staticmethod
    def execute():
        controller = SQLSERVERDBModel()
        subprocess.call([r'C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat'])

        prompt = "Cliente- Alo ? Agente- Buenos Dias."

        for line in controller.test():
            print(line)
            final_wavs = RecordingModel.get_recordings(str(line[3]), str(line[4]))
            print(final_wavs)
            if final_wavs is not None:
                for final_wav in final_wavs:
                    audio = AudioGPTRequestModel(prompt, final_wav.path, final_wav.name)
                    audio_response = OpenAIRequestCreator.audio_request(audio)
                    audio.set_response(audio_response)

                    prompt = "Un agente esta hablando con un cliente, dame solo la conversación del agente"
                    get_only_agent_req = ChatGPTRequestModel(prompt, audio.get_response(), final_wav.name)
                    chat_response = OpenAIRequestCreator.chat_request(get_only_agent_req)
                    get_only_agent_req.set_response(chat_response)

                    positive_phrases_model = EncouragedPhrasesModel(final_wav.name, get_only_agent_req.get_response())
                    positive, ticket_positive = EncouragedPhrasesController.calculate_score(positive_phrases_model)
                    negative_phrases_model = ProhibitedPhrasesModel()
                    negative = ProhibitedPhrasesController.calculate_score(get_only_agent_req.get_response())

                    total = negative + positive

                    positive_phrases_model.set_phrase_score(total, ticket_positive)


QualityAssurance.execute()
