from backend.Model.DB.PostGreSQLModel import PostGre
from backend.Controller.pathFinder import JSONFinder
from backend.Model.DB.recordingsDB import Recording, Embedding


class PostgreController:

    @classmethod
    def add_recording(cls, gestion_id: str, name: str, audio_text: dict = None) -> Recording:
        postgre = PostGre()
        phone_location = name.find('09')
        temp_cell = ""
        if phone_location == -1:
            new_phone_location = name.find('9')
            if new_phone_location != -1:
                for i in range(0, 9):
                    if name[new_phone_location+i].isdigit():
                        temp_cell += name[new_phone_location+i]
        else:
            for i in range(0, 10):
                if name[phone_location+i].isdigit():
                    temp_cell += name[phone_location+i]

        if len(temp_cell) >= 9:
            cellphone = temp_cell
        else:
            cellphone = None
        return postgre.add_recording(gestion_id, audio_text, cellphone, name)

    @staticmethod
    def get_recording_row(name: str):
        postgre = PostGre()
        return postgre.get_recording_given_name(name).first()

    @staticmethod
    def add_audio_text(recording_id: str, audio_text: dict):
        postgre = PostGre()
        return postgre.update_recording_audio_text(recording_id, audio_text)
    @staticmethod
    def get_audio_text(recording_id: str):
        postgre = PostGre()
        return postgre.get_audio_text(recording_id).first()


    @staticmethod
    def add_embedding(recording_id: str, embedding: dict) -> Embedding:
        postgre = PostGre()
        return postgre.add_embedding(recording_id, embedding)

    @staticmethod
    def get_embedding(name: str):
        postgre = PostGre()
        return postgre.get_embedding(name).first()

    @staticmethod
    def add_scores(recording_id: str, score: dict):
        postgre = PostGre()
        postgre.add_scores(recording_id, score)

    @staticmethod
    def get_scores(name: str):
        pass

    @classmethod
    def add_qa_processes(cls, gestion_id: str, name: str, score: dict):
        postgre = PostGre()

        gestion = cls.add_embedding(gestion_id, name)

        jsonfinder = JSONFinder("../analysed_records/audio_text")

        audio = jsonfinder.find(name)

        postgre.add_scores(gestion.id, audio)

        postgre.close()

    @staticmethod
    def get_pa_processes(y: str, m: str, d: str):
        postgre = PostGre()
        return postgre.get_scores(y, m, d)

    @staticmethod
    def get_recordings_given_date(y: str, m: str, d: str):
        postgre = PostGre()
        return postgre.get_recordings_given_date(y, m, d)





