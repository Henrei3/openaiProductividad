from backend.Model.DB.PostGreSQLModel import PostGre
from backend.Controller.pathFinder import JSONFinder
from backend.Model.DB.recordingsDB import Recording, Embedding, Scores


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
    def get_recording(name: str) -> Recording:
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
    def add_scores(score: Scores):
        postgre = PostGre()
        previusly_existing_score = postgre.get_score(score.s_id).first()
        if previusly_existing_score:
            return postgre.update_score(score)
        return postgre.add_score(score)

    @staticmethod
    def get_scores(y: str, m: str, d: str):
        pass

    @staticmethod
    def get_pa_processes(y: str, m: str, d: str):
        postgre = PostGre()
        return postgre.get_scores_given_date(y, m, d)

    @staticmethod
    def get_recordings_given_date(y: str, m: str, d: str):
        postgre = PostGre()
        return postgre.get_recordings_given_date(y, m, d)
