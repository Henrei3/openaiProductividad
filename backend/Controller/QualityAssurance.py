from backend.Model.RecordingModel import RecordingModel
from backend.Model.AudioGPTRequestModel import AudioGPTRequestModel
from backend.Model.DataBase import SQLSERVERDBModel
from backend.Controller.GPTCreator import OpenAIRequestCreator
from backend.Controller.PhrasesController import EncouragedPhrasesController
from backend.Controller.PhrasesController import ProhibitedPhrasesController


class QualityAssurance:

    @staticmethod
    def execute():
        controller = SQLSERVERDBModel()

        prompt = "Cliente- Alo ? Agente- Buenos Dias. (Español)"

        for line in controller.get_all_recordings_given_date('2023', '04', '27'):
            print(line)
            final_wav = RecordingModel.get_recording(str(line[3]), str(line[4]))
            print(final_wav)
            if final_wav is not None:
                audio = AudioGPTRequestModel(prompt, final_wav[1], final_wav[0])
                response = OpenAIRequestCreator.audio_request(audio)
                audio.set_response(response)

                positive, ticket_positive = EncouragedPhrasesController.calculate_score(audio.get_response())
                negative = ProhibitedPhrasesController.calculate_score(audio.get_response())

                total = negative + positive

                audio.set_score(total, ticket_positive)

