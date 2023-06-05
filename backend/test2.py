from backend.Model.DB.base import engine, Session
from backend.Model.DB.recordingsDB import Base, Gestion, PatronesExito, Contenido
from sqlalchemy import text
from backend.Model.RecordingModel import RecordingModel
from backend.Model.DB.SQLServer import SQLSERVERDBModel
from backend.Controller.PhrasesController import EncouragedPhrasesController
from backend.Controller.PhrasesController import ProhibitedPhrasesController
from backend.Model.PhrasesModel import EncouragedPhrasesModel, ProhibitedPhrasesModel
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.pathFinder import JSONFinder
from backend.Controller.PossibleWav import PossibleWav


class FlaskTesting:
    @staticmethod
    def make_post_simple():
        url = "http://127.0.0.1:5000/records"

        audio_text = {"content": "Alo ?"}
        score = {"QA": "Dos tablas "}

        simple_post_object = Gestion(10, 10, 10, 10)


class PostGreDataBaseTesting:

    @staticmethod
    def add_real_record():

        session = Session()

        Base.metadata.create_all(engine)
        cellphone = "34567832"
        gestion = Gestion(cellphone)
        session.add(gestion)
        session.commit()

        jsonfinder = JSONFinder("./analysed_records/scores")
        score = jsonfinder.find("out-0980427196")
        jsonfinder = JSONFinder("./analysed_records/audio_text")
        audio_text = jsonfinder.find("out-0980427196")
        name = "out-0980427196"
        gpt_answer = None
        audio = Contenido(gestion.g_id, name, audio_text, score, gpt_answer)
        session.add(audio)
        session.commit()
        session.close()

        PostGreDataBaseTesting.see_q_a_info()

    @staticmethod
    def see_q_a_info():
        session = Session()

        gestion = session.query(Gestion).all()
        audios = session.query(Contenido).all()

        print("## Gestion")
        for calidad in gestion:
            print(f"{calidad.g_id}:  {calidad.cellphone}")

        print("## Audios")
        for audio in audios:
            print(f"{audio.g_id} : {audio.name} - {audio.audio_text} - {audio.score} - {audio.gpt_answer}")

    @staticmethod
    def see_patterns():
        sess = Session()
        gestion = sess.query(Gestion).all()
        patrones_exito = sess.query(PatronesExito).all()

        print("## PatronesExito")
        for patrones in patrones_exito:
            print(f"{patrones.pe_id}: {patrones.patterns}")

        print("## Gestion")
        for calidad in gestion:
            print(f"{calidad.g_id}:  {calidad.score}")

    @staticmethod
    def create_tables():
        Base.metadata.create_all(engine)

    @staticmethod
    def delete_tables():
        Contenido.__table__.drop(engine)
        Gestion.__table__.drop(engine)

    @staticmethod
    def reset_all_tables():
        PostGreDataBaseTesting.delete_tables()
        PostGreDataBaseTesting.create_tables()

    @staticmethod
    def read_tables():
        session = Session()

        everything = session.execute(text("select * from gestion left join contenido on gestion.id = contenido.g_id"))

        for one in everything:
            print(one)


class QualityAssuranceTest:

    @staticmethod
    def json_managing_test():

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
    def score_calculation_not_found_cedente_test():

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


QualityAssuranceTest.score_calculation_not_found_cedente_test()
