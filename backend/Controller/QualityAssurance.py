from backend.Model.RecordingModel import RecordingModel
from backend.Model.RequestModel import AudioGPTRequestModel, OpenAIModelInterface
from backend.Model.DB.SQLServer import SQLSERVERDBModel
from backend.Controller.GPTCreator import OpenAIAudioRequest, OpenAIProxyAudio, OpenAIProxyEmbeddings
from backend.Controller.PhrasesController import EncouragedPhrasesController
from backend.Controller.PhrasesController import ProhibitedPhrasesController
from backend.Model.PhrasesModel import EncouragedPhrasesModel, ProhibitedPhrasesModel
from backend.Controller.PostGreSQLController import PostgreController
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.PossibleWav import PossibleWav
from backend.Controller.SQLServerController import SQLServerController
from backend.Controller.analyser import SpeechRefinement
import subprocess
import time


class QualityAssurance:

    @staticmethod
    def execute(y: str, m: str, d: str):
        sql_server_model = SQLSERVERDBModel()
        prompt = "Cliente-Alo ? Agente-Buenos Dias..."
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")
        for line in sql_server_model.get_all_recordings_given_date(y, m, d):
            print(line)
            phone_number = str(line[3])
            date = str(line[4])
            final_wavs = PossibleWav.get_recordings(phone_number, date)
            if final_wavs is not None:
                for final_wav in final_wavs:
                    """ Speech to Text """
                    audio: OpenAIModelInterface = AudioGPTRequestModel(
                        prompt, final_wav.path, final_wav.name, final_wav.size
                    )
                    diarized_speech = OpenAIProxyAudio.check_access(audio, True)

                    """ Score Calculation """
                    recording = RecordingModel(final_wav.name)
                    positive_phrases_model = EncouragedPhrasesModel(diarized_speech, str(line[5]))
                    positive, ticket_positive = EncouragedPhrasesController.calculate_score(positive_phrases_model)
                    negative_phrases_model = ProhibitedPhrasesModel(diarized_speech)
                    negative = ProhibitedPhrasesController.calculate_score(negative_phrases_model)

                    total = positive + negative
                    gestion_id = int(line[0])
                    recording.set_score(total, ticket_positive, gestion_id)
            else:
                print(final_wavs)

    @staticmethod
    def await_test():
        processes_given_date = PostgreController.get_pa_processes("2023", "04", "27")
        processed_view = dict()
        for process in processes_given_date:
            processed_view[process[1]] = [process[2], process[3]]
        print(processed_view)
        return processed_view
