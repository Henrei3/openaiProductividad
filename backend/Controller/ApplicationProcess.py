from backend.Controller.PhrasesController import EncouragedPhrasesController, ProhibitedPhrasesController
from backend.Model.PhrasesModel import EncouragedPhrasesModel, ProhibitedPhrasesModel
from backend.Model.RecordingModel import RecordingModel
from backend.Model.RequestModel import AudioGPTRequestModel
from backend.Model.RequestModel import EmbeddingRequestModel
from backend.Model.DB.SQLServer import SQLSERVERDBModel
from backend.Model.DB.recordingsDB import Recording
from backend.Model.jsonCreator import JsonFileCreator
from backend.Controller.PostGreSQLController import PostgreController
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.PossibleWav import PossibleWav, WavModel
from backend.Controller.GPTCreator import OpenAIProxyAudio, OpenAIProxyEmbeddings
from backend.Controller.GPTCreator import OpenAIModelInterface, OpenAIEmbeddingRequest
from abc import ABC, abstractmethod
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.analyser import PatternController
import subprocess
import json
import os


class ApplicationProcess(ABC):

    @staticmethod
    @abstractmethod
    def setup_application(y: str, m: str, d: str):
        pass

    @classmethod
    def audio_price_evaluation(cls, y: str, m: str, d: str):
        """ This method will search for all the pertinent records inside the database that were
                 recorded in a certain date the format must be y - m - d.
                 returns the price that it takes to transform all those recordings into text"""
        total_price = 0
        for line in cls.setup_application(y, m, d):
            phone_number = str(line[3])
            date = str(line[4])

            wavs = PossibleWav.get_recordings(phone_number, date)
            gestion_id = line[0]
            recordings = list()

            if wavs:
                for audio_file in wavs:
                    audio_gpt: OpenAIModelInterface = AudioGPTRequestModel(
                        prompt="", audio_path=audio_file.path, name=audio_file.name, size=audio_file.size
                    )
                    # We send to the database the recording data
                    audio_gpt.set_recording(gestion_id)

                    proxy_response = OpenAIProxyAudio.check_access(audio_gpt, False)

                    if type(proxy_response) is float:
                        total_price += proxy_response
                    recordings.append(audio_file.deserialize())
                JsonFileCreator.write(recordings, "../analysed_records/wav_data.json")

        return total_price


class GestionesDePago(ApplicationProcess):

    @staticmethod
    def setup_application(y: str, m: str, d: str):
        date_for_storage = {"y": y, "m": m, "d": d}
        JsonFileCreator.write(date_for_storage, "../analysed_records/date.json")
        sql_server_model = SQLSERVERDBModel()
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")
        return sql_server_model.get_all_successfull_recordings_given_date(y, m, d)

    @staticmethod
    def audio_transformation_embeddings_evaluation():
        """ This method should only be executed once the price of this transaction is calculated and the WavFiles are
         stored, it calls the OpenAI api and transforms all the records.
         It returns the price of turning these recordings into embeddings"""

        prompt = "Cliente-Alo ? Agente-Buenos Dias..."
        json_finder = JSONFinder("../analysed_records")
        wavs_data = json_finder.find("wav_data")
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")

        total_price = 0
        for recording in wavs_data:
            wav_file = WavModel.serialize(recording)

            audio: OpenAIModelInterface = AudioGPTRequestModel(prompt, wav_file.path, wav_file.name)
            audio_proxy_response = OpenAIProxyAudio.check_access(audio, True)
            embedding: OpenAIModelInterface = EmbeddingRequestModel(wav_file.name, audio_proxy_response)
            embedding_proxy_response = OpenAIProxyEmbeddings.check_access(embedding, False)
            print(embedding_proxy_response)
            if type(embedding_proxy_response) is float:
                total_price += embedding_proxy_response

        return total_price

    @staticmethod
    def embeddings_calculation():
        """ This method is the last method of the pattern management section.
        It should be done once all the other part are completed.
        This method takes all the recordings with their audio translated
        stored in the database of a certain date and transforms them into embeddings
        the result is stored in the database"""

        json_finder = JSONFinder("../analysed_records/")
        dates = json_finder.find('date')

        chunked_iterator_results = PostgreController.get_recordings_given_date(dates['y'], dates['m'], dates['d'])
        for row_results in chunked_iterator_results:
            recording: Recording = row_results[0]
            embedding_request = EmbeddingRequestModel(recording.name, recording.audio_text)
            proxy_response = OpenAIProxyEmbeddings.check_access(embedding_request, True)
            print(proxy_response)


class QualityAssurance(ApplicationProcess):

    @staticmethod
    def setup_application(y: str, m: str, d: str):
        sql_server_model = SQLSERVERDBModel()
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")
        return sql_server_model.get_all_recordings_given_date(y, m, d)

    @staticmethod
    def execute(y: str, m: str, d: str):
        sql_server_model = SQLSERVERDBModel()
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")
        for line in sql_server_model.get_all_recordings_given_date(y, m, d):
            prompt = "Cliente-Alo ? Agente-Buenos Dias..."
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


audio_price = QualityAssurance.audio_price_evaluation('2023', '04', '27')
print(audio_price)