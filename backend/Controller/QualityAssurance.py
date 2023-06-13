import time

from backend.Model.RecordingModel import RecordingModel
from backend.Model.RequestModel import AudioGPTRequestModel
from backend.Model.DB.SQLServer import SQLSERVERDBModel
from backend.Controller.GPTCreator import OpenAIRequestCreator
from backend.Controller.PhrasesController import EncouragedPhrasesController
from backend.Controller.PhrasesController import ProhibitedPhrasesController
from backend.Model.PhrasesModel import EncouragedPhrasesModel, ProhibitedPhrasesModel
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.PostGreSQLController import PostgreController
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.PossibleWav import PossibleWav
from backend.Controller.SQLServerController import SQLServerController
import subprocess


class QualityAssurance:

    @staticmethod
    def execute(y, m, d):
        sql_server_model = SQLSERVERDBModel()
        prompt = "Cliente :-Alo ? Agente:-Buenos Dias..."
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")
        for line in sql_server_model.get_all_recordings_given_date(y, m, d):
            print(line)
            final_wavs = PossibleWav.get_recordings(str(line[3]), str(line[4]))
            if final_wavs is not None:
                for final_wav in final_wavs:
                    """ Speech to Text """
                    audio = AudioGPTRequestModel(prompt, final_wav.path, final_wav.name)
                    audio_response = OpenAIRequestCreator.audio_request(audio)
                    audio.set_response(audio_response)

                    """ Refining Speech so That only the agent speech is collected """
                    refined_speech = SpeechRefinement.get_only_agent(audio.get_response())

                    """ Score Calculation """
                    recording = RecordingModel(final_wav.name)
                    positive_phrases_model = EncouragedPhrasesModel(refined_speech, str(line[5]))
                    positive, ticket_positive = EncouragedPhrasesController.calculate_score(positive_phrases_model)
                    negative_phrases_model = ProhibitedPhrasesModel(refined_speech)
                    negative = ProhibitedPhrasesController.calculate_score(negative_phrases_model)

                    total = positive + negative
                    gestion_id = int(line[0])
                    recording.set_score(total, ticket_positive, gestion_id)
            else:
                print(final_wavs)
        """ Sending Info to The PostGreSQL and SQLServer Databases once all audios treated """
        jsonfinder = JSONFinder("../analysed_records/scores")
        for scores in jsonfinder.findAll_plus_name():
            name = scores[0]
            json_object = scores[1]
            gestion_id = json_object.pop('gestion_id')

            PostgreController.add_qa_processes(gestion_id, name, json_object)
            SQLServerController.add_qa_processes(gestion_id, name, json_object)

            server_model = SQLSERVERDBModel()
            everything = server_model.get_grabaciones()
            for one in everything:
                print(one)

            everywhere = server_model.get_autogenerated_scores()
            for at_the_same_time in everywhere:
                print(at_the_same_time)
    @staticmethod
    def await_test():
        processes_given_date = PostgreController.get_pa_processes("2023", "04", "27")
        processed_view = dict()
        for process in processes_given_date:
            processed_view[process[1]] = [process[2], process[3]]
        print(processed_view)
        return processed_view
