from backend.Model.RequestModel import AudioGPTRequestModel
from backend.Model.RequestModel import EmbeddingRequestModel
from backend.Model.DB.SQLServer import SQLSERVERDBModel
from backend.Model.jsonCreator import JsonFileCreator
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.PossibleWav import PossibleWav,WavModel
from backend.Controller.GPTCreator import OpenAIProxyAudio, OpenAIProxyEmbeddings, OpenAIModelInterface, OpenAIEmbeddingRequest
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.analyser import PatternController
from decouple import config
import subprocess
import json
import os


class GestionesDePago:

    @staticmethod
    def gestiones_de_pago():
        prompt = "Cliente- Alo ? Agente- Buenos Dias"

        wavs = PossibleWav.get_recordings()
        for audio_file in wavs:
            """ Speech To Text """
            audio_gpt: OpenAIModelInterface = AudioGPTRequestModel(prompt, audio_file.path, audio_file.name)
            audio_response = OpenAIProxyAudio.check_access(audio_gpt, True)

            """ text IA text """
            embedding_gpt = EmbeddingRequestModel(audio_file.name, audio_response)
            chat_response = OpenAIEmbeddingRequest.execute_request(embedding_gpt)

            """  Patterns """
            PatternController.countWords(audio_file.name)

    @staticmethod
    def audio_price_evaluation(y: str, m: str, d: str) -> float:
        """ This method will search for all the pertinent records inside the database that were
         recorded in y - m - d date. returns the price that it takes to transform all those recordings into text"""

        sql_server_model = SQLSERVERDBModel()
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")
        for line in sql_server_model.get_all_successfull_recordings_given_date(y, m, d):
            phone_number = str(line[3])
            date = str(line[4])
            gestion_id = line[0]
            wavs = PossibleWav.get_recordings(phone_number, date)
            recordings = list()
            total_price = 0
            for audio_file in wavs:
                audio_gpt: OpenAIModelInterface = AudioGPTRequestModel(
                    prompt="", audio_path=audio_file.path, name=audio_file.name
                )
                # We send to the database the recording data
                audio_gpt.set_recording(gestion_id)
                proxy_response = OpenAIProxyAudio.check_access(audio_gpt, False)

                if type(proxy_response) is float:
                    total_price += proxy_response
                recordings.append(audio_file.deserialize())
            JsonFileCreator.write(recordings, "../analysed_records/wav_data.json")

            return total_price

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
            print(embedding)
            embedding_proxy_response = OpenAIProxyEmbeddings.check_access(embedding, False)
            print(embedding_proxy_response)
            if type(embedding_proxy_response) is float:
                total_price += embedding_proxy_response

        return total_price


audio_price = GestionesDePago.audio_price_evaluation('Test', 'Test', 'Test')
print(audio_price)

