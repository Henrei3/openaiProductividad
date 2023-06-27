from backend.Model.DB.base import engine, Session
from backend.Model.DB.recordingsDB import Base, Recording, Embedding, Scores
from backend.Model.RecordingModel import RecordingModel
from backend.Model.DB.SQLServer import SQLSERVERDBModel
from backend.Controller.PhrasesController import EncouragedPhrasesController
from backend.Controller.PhrasesController import ProhibitedPhrasesController
from backend.Model.PhrasesModel import EncouragedPhrasesModel, ProhibitedPhrasesModel
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.PossibleWav import PossibleWav
from backend.Model.RequestModel import OpenAIModelInterface, ChatGPTRequestModel, AudioGPTRequestModel
from backend.Controller.GPTCreator import OpenAIProxy, OpenAIProxyAudio, OpenAIProxyEmbeddings
from sqlalchemy import text, select
import subprocess
import unittest
import pathlib
import shutil
import os


class FlaskTesting:
    @staticmethod
    def make_post_simple():
        url = "http://127.0.0.1:5000/records"

        audio_text = {"content": "Alo ?"}
        score = {"QA": "Dos tablas "}


class PostGreDataBaseTesting(unittest.TestCase):

    def test_add_record_audio_text_none(self):
        session = Session()

        query = select(Recording).where(Recording.g_id == "2222")

        query_result = session.execute(query)
        recording_object = query_result.first()
        if recording_object is None:
            recording = Recording('2222', None, '0995205649', 'out-something')

            session.add(recording)
            session.commit()

            query_result = session.execute(query)

            recording_object = query_result.first()
        self.assertEquals(recording_object[0].g_id, 2222)

    def test_see_q_a_info(self):
        session = Session()

        gestion = session.query(Recording).all()
        audios = session.query(Scores).all()

        print("## Gestion")
        for calidad in gestion:
            print(f"{calidad.g_id}:  {calidad.cellphone}")

        print("## Audios")
        for audio in audios:
            print(f"{audio.g_id} : {audio.name} - {audio.audio_text} - {audio.score} - {audio.gpt_answer}")

    def test_see_patterns(self):
        sess = Session()
        gestion = sess.query(Recording).all()
        patrones_exito = sess.query(Embedding).all()

        print("## PatronesExito")
        for patrones in patrones_exito:
            print(f"{patrones.e_id}: {patrones.embedding}")

        print("## Gestion")
        for calidad in gestion:
            print(f"{calidad.id}:  {calidad.g_id} - {calidad.audio_text} - {calidad.cellphone} - {calidad.name} ")

    def test_create_tables(self):
        Base.metadata.create_all(engine)

    def test_delete_tables(self):
        Scores.__table__.drop(engine)
        Embedding.__table__.drop(engine)
        Recording.__table__.drop(engine)

    def test_delete_patrones(self):
        Embedding.__table__.drop(engine)

    def test_reset_all_tables(self):
        self.test_delete_tables()
        self.test_create_tables()

    @staticmethod
    def read_tables():
        session = Session()

        everything = session.execute(text("select * from gestion left join contenido on gestion.id = contenido.g_id"))

        for one in everything:
            print(one)


class QualityAssuranceTest(unittest.TestCase):

    def test_json_managing_test(self):

        controller = SQLSERVERDBModel()

        for line in controller.get_all_recordings_given_date("2023", "04", "27"):
            final_wavs = PossibleWav.get_recordings(str(line[3]), str(line[4]))
            if final_wavs is not None:
                print(line)
                print(final_wavs)
                for final_wav in final_wavs:
                    json_finder = JSONFinder("./analysed_records/scores")
                    print(final_wav.name)
                    score = json_finder.find(final_wav.name)
                    recording = RecordingModel(final_wav.name)
                    total = score['total']
                    ticket_score = score['ticket_score']
                    print(line[0])
                    recording.set_score(total, ticket_score, int(line[0]))

    @staticmethod
    def test_score_calculation_not_found_cedente_test():

        controller = SQLSERVERDBModel()

        for line in controller.get_all_recordings_given_date("2023", "04", "27"):
            final_wavs = PossibleWav.get_recordings(str(line[3]), str(line[4]))
            if final_wavs is not None:
                print(line)
                print(final_wavs)
                for final_wav in final_wavs:
                    jsonfinder = JSONFinder("./analysed_records/audio_text/")

                    speech: str = ""

                    for json_object in jsonfinder.findAll():
                        speech = json_object['text']

                    refined_speech = SpeechRefinement.refine_speech_textOpenAI(speech)

                    recording = RecordingModel(final_wav.name)
                    positive_phrases_model = EncouragedPhrasesModel(refined_speech, str(line[5]))
                    positive, ticket_positive = EncouragedPhrasesController.calculate_score(positive_phrases_model)
                    negative_phrases_model = ProhibitedPhrasesModel(refined_speech)
                    negative = ProhibitedPhrasesController.calculate_score(negative_phrases_model)

                    total = positive + negative
                    gestion_id = int(line[0])
                    recording.set_score(total, ticket_positive, gestion_id)


class ProxyPatternTests(unittest.TestCase):
    def test_proxy_pattern_already_existing(self):
        controller = SQLSERVERDBModel()
        prompt = "Cliente-Alo ? Agente-Buenos Dias"
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")
        for line in controller.test():
            final_wavs = PossibleWav.get_recordings(str(line[3]), str(line[4]))
            if final_wavs is not None:
                print(line)
                for final_wav in final_wavs:

                    audio = AudioGPTRequestModel(prompt, final_wav.path, final_wav.name)
                    diarized_test = OpenAIProxyAudio.operation(audio, False)

                    print(diarized_test)

                    self.assertTrue(type(diarized_test) is str)

                    self.assertTrue(len(diarized_test) > 50)

    def test_proxy_pattern_unexisting(self):
        path = '../analysed_records/audio_text'
        if os.path.exists(path):
            self._delete_folder_with_content(path)
        self.test_proxy_pattern_already_existing()

    def test_score_calculation(self):
        pass

    @staticmethod
    def _delete_folder_with_content(path_to_folder):
        folder = path_to_folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        os.rmdir(path_to_folder)
